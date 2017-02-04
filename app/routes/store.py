from flask import session, redirect, url_for, render_template, request, jsonify, Response, flash, Blueprint
import requests
import json


store = Blueprint('store', __name__)
DB_BASE_URL = 'https://lotgul9df8.execute-api.us-west-2.amazonaws.com/prod/'


@store.route('/store', methods=['GET'])
def list_items():
	r = requests.get(DB_BASE_URL + '/storeItems')
	store_items = json.loads(r.json())['Items']
	print(store_items)
	return render_template('store.html', storeItems=store_items)
