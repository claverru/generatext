FROM python:3.6-slim

RUN apt-get update
RUN apt-get install -y gcc

ADD requirements.txt .
RUN pip install -r requirements.txt

RUN python -m spacy download es

CMD bash