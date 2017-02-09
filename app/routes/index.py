from flask import session, redirect, url_for, render_template, request, jsonify, Response, flash, Blueprint
import requests
import json


index = Blueprint('index', __name__)


@index.route('/', methods=['GET'])
def landing():
	return render_template('index.html')
