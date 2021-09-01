#!/bin/sh
mongod --fork --logpath /webservice/volume/mongo.log
python3 service.py
