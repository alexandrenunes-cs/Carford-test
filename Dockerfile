FROM python:3.8.6-slim-buster

RUN pip install pipenv

WORKDIR /app
COPY app/Pipfile .
RUN pipenv install

COPY app/ .
ENTRYPOINT pipenv run uvicorn main:app --host 0.0.0.0 --port $PORT --reload --log-level info --log-config logging.conf
