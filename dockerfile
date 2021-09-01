# Build image with command
#   docker build -t cost_service .
# Run container with command
#   docker run -dp 80:8080 cost_service

FROM ubuntu:latest
MAINTAINER avagadro 'p-avagadro@yandex.com'

# install python3
RUN apt-get update -y
RUN apt-get install -y python3-pip python3-dev build-essential vim

# prepare environment: copy files, install requirements
COPY *.py /webservice/
COPY requirements.txt /webservice/
COPY static/ /webservice/static/
COPY templates/* /webservice/templates/
RUN mkdir /webservice/volume
VOLUME /webservice/volume
WORKDIR /webservice

RUN pip3 install -r requirements.txt

# set entrypoint
ENTRYPOINT ["python3", "service.py"]



# install Python3
# RUN apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv 7F0CEB10
# RUN apt-key list | grep "expired: " | sed -ne 's|pub .*/\([^ ]*\) .*|\1|gp' | xargs -n1 apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys
# RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys
# RUN apt-get update
# RUN apt-get install -y python3 python3-pip python3-dev
