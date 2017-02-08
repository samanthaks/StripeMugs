from flask import Flask, jsonify, request, Blueprint, redirect, url_for
from flask_jwt_extended import JWTManager, jwt_required,\
	create_access_token, get_jwt_identity, set_access_cookies
from .. import app


# Setup the Flask-JWT-Extended extension
jwt = JWTManager(app)
auth = Blueprint('auth', __name__)


# Provide a method to create access tokens. The create_access_token()
# function is used to actually generate the token
@auth.route('/login', methods=['POST'])
def login():
	username = request.form['username']
	password = request.form['password']
	if username != '1@test.com' or password != 'test':
		return jsonify({"msg": "Bad username or password"}), 401

	# Identity can be any data that is json serializable
	access_token = create_access_token(identity=username)
	ret = {'access_token': access_token}
	resp = jsonify(ret)
	set_access_cookies(resp, access_token)
	print resp.data

	return redirect(url_for('store.list_items'))


# Protect a view with jwt_required, which requires a valid access token
# in the request to access.
@auth.route('/protected', methods=['GET'])
@jwt_required
def protected():
	# Access the identity of the current user with get_jwt_identity
	current_user = get_jwt_identity()
	return jsonify({'current_user': current_user}), 200


if __name__ == '__main__':
	app.run()
