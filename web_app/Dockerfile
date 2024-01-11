FROM python:3.8
WORKDIR /usr/src/app
COPY requirements.txt .
RUN pip3 install -r requirements.txt
RUN apt-get update && apt-get install -y
RUN apt install netcat-traditional # used to ping db service
COPY . .