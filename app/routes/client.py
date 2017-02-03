from flask import session, redirect, url_for, render_template, request, jsonify, Response, flash, Blueprint
# from ..forms import CreateForm
# from ..models import Player


client = Blueprint('client', __name__)


@client.route('/', methods=['GET'])
def index():
	return render_template('index.html')
