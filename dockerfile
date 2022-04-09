FROM python:3.9-slim
MAINTAINER fragarie 'fragarie@yandex.com'

# prepare environment: copy files, install requirements
RUN python3 -m venv /intravel/venv
COPY requirements.txt /costservice/
RUN /intravel/venv/bin/pip3 install -r /intravel/requirements.txt
COPY . /intravel/
WORKDIR /intravel

ENTRYPOINT ["/intravel/venv/bin/python3", "service.py"]
