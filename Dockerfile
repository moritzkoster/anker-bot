FROM python:3.8

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY python python
COPY settings.json settings.json 

COPY main.py main.py

CMD [ "python3", "main.py"]

