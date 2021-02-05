FROM python:3.9.1-alpine

COPY requirements.txt /code/

RUN pip install -r /code/requirements.txt
