FROM python:3.11-slim

WORKDIR /app

COPY /server/server.py /app
COPY requirements.txt /app

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python", "server.py"]