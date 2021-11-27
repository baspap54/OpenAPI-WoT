from flask import Flask, jsonify, request, session, render_template, make_response 
import json
import random, string
import logging
import sys
import requests
from random import randrange
from markupsafe import escape
from datetime import datetime 
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import socket

app = Flask(__name__) # create an app instance
app.config['MONGO_URI'] = "mongodb://mongo:27017/mongo"

mongo = PyMongo(app)

@app.route("/")
def index():
    return '''
    	<form method="POST" action="/create" enctype="multipart/form-data">
    	<input type="file" name="OpenAPI_document">  
    	<input type="submit">
    	</form>
    '''

@app.route('/create', methods=['POST'])
def create():
	if 'OpenAPI_document' in request.files:
		OpenAPI_document = request.files['OpenAPI_document']
		mongo.save_file(OpenAPI_document.filename, OpenAPI_document)
		mongo.db.things.insert({'OpenAPI_document_name' : OpenAPI_document.filename})
	return 'Done!'
    

@app.route('/things/<filename>')
def filename(filename):
	return mongo.send_file(filename)


