FROM python:latest

COPY . /home/cjws/
ENV AWS_ACCESS_KEY_ID $AWS_ACCESS_KEY_ID
ENV AWS_SECRET_ACCESS_KEY $AWS_SECRET_ACCESS_KEY
WORKDIR /home/cjws/
RUN pip install -r requirements.txt


