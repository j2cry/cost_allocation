# Build image with command
#   docker build -t cost_service .
# Run container with command
#   docker run -dp 80:8080 cost_service

FROM ubuntu:latest
MAINTAINER avagadro 'p-avagadro@yandex.com'

# install python3
RUN apt-get update -y
RUN apt-get install -y python3-pip python3-dev build-essential vim gnupg wget

# prepare environment: copy files, install requirements
COPY *.py /webservice/
COPY requirements.txt /webservice/
COPY static/ /webservice/static/
COPY templates/* /webservice/templates/
RUN mkdir /webservice/volume
VOLUME /webservice/volume
WORKDIR /webservice
RUN pip3 install -r requirements.txt

ENTRYPOINT ["python3", "service.py"]

# # To build MongoDB and flask app in one container uncomment the code below
# # Please note that this is highly undesirable, since you will have to update the application manually.
# # Otherwise, you the data stored in mongodb may be lost.

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
# COPY start.sh /webservice/
# RUN chmod +x start.sh
# ENTRYPOINT ["./start.sh"]
