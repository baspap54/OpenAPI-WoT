from flask import Flask, jsonify, request, session, render_template, make_response, render_template, redirect, url_for, flash
import json
import os
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
from werkzeug.utils import secure_filename

app = Flask(__name__) # create an app instance
app.config['MONGO_URI'] = "mongodb://mongo:27017/mongo"
app.config['UPLOAD_EXTENSIONS'] = ['.json', '.yml']
app.secret_key = 'secret_key'
mongo = PyMongo(app)

@app.route("/")
def index():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload():
	OpenAPI_document = request.files['file']
	if OpenAPI_document.filename != '':
		file_ext = os.path.splitext(OpenAPI_document.filename)[1]
		if file_ext not in app.config['UPLOAD_EXTENSIONS']:
			flash("This is not an OpenAPI document!")
			return redirect(url_for('index'))
		mongo.save_file(OpenAPI_document.filename, OpenAPI_document)
		mongo.db.things.insert({'OpenAPI_document_name' : OpenAPI_document.filename})
		flash("File uploaded!")
		return redirect(url_for('index'))
	flash("No file selected")
	return redirect(url_for('index'))

@app.route('/things/<filename>')
def filename(filename):
	return mongo.send_file(filename)


