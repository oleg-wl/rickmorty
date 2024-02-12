# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN pip install --upgrade pip
RUN pip install pipenv
COPY . /app

RUN pipenv install --deploy --ignore-pipfile

CMD ["pipenv" , "run", "python", "app.py"]