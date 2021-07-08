FROM python:3.8-slim-buster
MAINTAINER Burlakov Eugene

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

RUN python -m unittest tests -q

ENTRYPOINT python main.py --periods 3
