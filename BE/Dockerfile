FROM python:3.9-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

COPY .env /app/.env

EXPOSE 5000

CMD ["python", "main.py"]
