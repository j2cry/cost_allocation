FROM python:3.9-slim
MAINTAINER fragarie 'fragarie@yandex.com'

# prepare environment: copy files, install requirements
RUN python3 -m venv /costservice/venv
COPY requirements.txt /costservice/
RUN /costservice/venv/bin/pip3 install -r /costservice/requirements.txt
COPY . /costservice/
WORKDIR /costservice

ENTRYPOINT ["/costservice/venv/bin/python3", "service.py"]
