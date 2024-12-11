# Usar uma imagem base do Node.js para construir o FrontEnd
FROM node:18

# Definir o diretório de trabalho
WORKDIR /app

# Copiar os arquivos do FrontEnd para o container
COPY . /app

# Instalar dependências e construir o FrontEnd
RUN npm install
RUN npm run build

# Usar uma imagem NGINX para servir os arquivos estáticos
FROM nginx:alpine
COPY --from=0 /app/dist /usr/share/nginx/html

# Expor a porta do NGINX
EXPOSE 80

# Comando para rodar o NGINX
CMD ["nginx", "-g", "daemon off;"]
