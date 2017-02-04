from flask import session, redirect, url_for, render_template, request, jsonify, Response, flash, Blueprint
import pprint
import requests
import json


client = Blueprint('client', __name__)
DB_BASE_URL = 'https://lotgul9df8.execute-api.us-west-2.amazonaws.com/prod/'


@client.route('/', methods=['GET'])
def index():
	r = requests.get(DB_BASE_URL + '/storeItems')
	store_items = json.loads(r.json())['Items']
	print(store_items)
	return render_template('index.html', storeItems=store_items)
