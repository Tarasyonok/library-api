FROM python:3.12

RUN mkdir /library

WORKDIR /library

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .
