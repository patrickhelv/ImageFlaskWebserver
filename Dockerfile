FROM python:3.11-slim

WORKDIR /app
COPY /server/server.py /app 

RUN --mount=type=bind,source=requirements.txt,target=/tmp/requirements.txt \
pip install -r /tmp/requirements.txt

EXPOSE 5000

ENTRYPOINT ["python", "server.py"]