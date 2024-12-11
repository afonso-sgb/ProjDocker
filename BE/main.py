from flask import request, jsonify
from config import app, db
from models import Contact
from flask_cors import CORS

CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})


#get
@app.route("/contacts", methods=["GET"]) #decorator
def get_contacts():
    contacts = Contact.query.all() #uses flasksqlachemy to get all diferent contacts in db
    json_contacts = list(map(lambda x: x.to_json(), contacts)) #como contacts sao python objects é necessario convertelos para tipo json, map tira todos os elemetos da lista e aplica a funcao to_json a cada elemento
    return jsonify({"contacts": json_contacts})

#criar contacto
@app.route("/create_contact", methods=["POST"])
def create_contact():
    first_name = request.json.get("firstName")
    last_name = request.json.get("lastName")
    email = request.json.get("email")

    if not first_name or not last_name or not email:
        return( 
            jsonify({"message": "É necessário incluir primeiro nome, ultimo nome e email"}),
            400,
        )    

    new_contact = Contact(first_name=first_name, last_name=last_name, email=email) # quando queremos uma nova entrada na db criar um python class correspondente á entrada da db
    try:
        db.session.add(new_contact) #adicionado na sessao na db (staging area)
        db.session.commit() # write to db 
    except Exception as e:
        return jsonify ({"message": str(e)}), 400   #caso exista um erro no comit o except block avisa o user de erro

    return jsonify({"message": "Utilizador adicionado!"}), 201 


#update
@app.route("/update_contact/<int:user_id>", methods = ["PATCH"])
def update_contact(user_id):
    contact = Contact.query.get(user_id)

    if not contact:
       return jsonify({"message":"Utilizador não encontrado"}), 404
    
    data = request.json
    contact.first_name = data.get("firstName", contact.first_name)
    contact.last_name = data.get("lastName", contact.last_name)
    contact.email = data.get("email", contact.email)

    #como modificamso contact é necessario dar commit
    db.session.commit()

    return jsonify({"message":"Utilizador atualizado"}), 200


#delete
@app.route("/delete_contact/<int:user_id>", methods=["DELETE"])
def delete_contact(user_id):
    contact = Contact.query.get(user_id)

    if not contact:
       return jsonify({"message":"Utilizador não encontrado"}), 404
    
    db.session.delete(contact)
    db.session.commit()

    return jsonify({"message":"Utilizador Apagado"}), 200

if __name__ == "__main__":
    with app.app_context(): #quando comecamos a aplicacao vamos buscar o contexto e criamos todos os modulos definidos na base de dados 
        db.create_all()

    app.run(host="0.0.0.0", port=5000, debug=True) #run the code


 