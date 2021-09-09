# Build image with command
#   docker build -t cost_image .
# Run container with command
#   docker run -dp 80:8080 cost_image


# # Docker file for run MongoDB and Flask app in SEPARATE containers
FROM python:3.8-slim
MAINTAINER fragarie 'fragarie@yandex.com'

RUN apt-get update && apt-get install -y gcc vim

# prepare environment: copy files, install requirements
COPY . /webservice/
WORKDIR /webservice
RUN pip3 install -r requirements.txt

ENTRYPOINT ["python3", "service.py"]


# # Docker file for run MongoDB and Flask app in ONE container
# # Please note that this is highly undesirable, since you will have to update the application manually.
# # Otherwise, you the data stored in mongodb may be lost.
# FROM ubuntu:latest
# MAINTAINER fragarie 'fragarie@yandex.com'
#
# # install python3
# RUN apt-get update && apt-get install -y python3.8 python3-pip gnupg wget vim
#
# # prepare environment: copy files, install requirements
# COPY . /webservice/
# RUN mkdir /webservice/volume
# WORKDIR /webservice
# RUN pip3 install -r requirements.txt
#
# # Import MongoDB public GPG key AND create a MongoDB list file
# RUN wget -qO - https://www.mongodb.org/static/pgp/server-4.4.asc | apt-key add -
# RUN echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/4.4 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-4.4.list
#
# # Update apt-get sources AND install MongoDB
# RUN apt-get update && DEBIAN_FRONTEND="noninteractive" apt-get install -y mongodb-org
#
# # Create the MongoDB data directory
# RUN mkdir -p /data/db
# RUN mkdir -p /data/code
#
# # set entrypoint
# RUN chmod +x start.sh
# ENTRYPOINT ["./start.sh"]
