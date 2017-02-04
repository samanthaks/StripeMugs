from flask import session, redirect, url_for, render_template, request, jsonify, Response, flash, Blueprint
import requests
import json


index = Blueprint('index', __name__)
DB_BASE_URL = 'https://lotgul9df8.execute-api.us-west-2.amazonaws.com/prod/'


@index.route('/', methods=['GET'])
def landing():
	return render_template('index.html')
