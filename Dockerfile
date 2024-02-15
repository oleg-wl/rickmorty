# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED=1
ENV DEBUG=0

WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt

ENTRYPOINT ["./entrypoint.sh"]
