from flask import session, redirect, url_for, render_template, request, jsonify, Response, flash, Blueprint, session
import requests
import json
from flask_jwt_extended import JWTManager, jwt_required
from .. import db



store = Blueprint('store', __name__)


@store.route('/store', methods=['GET'])
@jwt_required
def list_items():
	items_dict = db.Table('items').scan()
	return render_template('store.html', storeItems=items_dict['Items'])
