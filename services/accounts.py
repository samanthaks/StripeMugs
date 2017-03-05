from flask import Flask, jsonify, request, Blueprint, redirect, url_for, session
from flask_jwt_extended import JWTManager, jwt_required,\
	create_access_token, get_jwt_identity, set_access_cookies, create_refresh_token, set_refresh_cookies, unset_jwt_cookies
from boto3.dynamodb.conditions import Key, Attr


# Setup the Flask-JWT-Extended extension
app = Flask(__name__)
jwt = JWTManager(app)


# Provide a method to create access tokens. The create_access_token()
# function is used to actually generate the token
@app.route('/login', methods=['POST'])
def login():
	username = request.form['username']
	password = request.form['password']

	user_dict = db.Table('Users').query(KeyConditionExpression=Key('email').eq(username))
	if(user_dict['Count'] == 1):
		if password == user_dict['Items'][0]['password']:
			# Identity can be any data that is json serializable
			access_token = create_access_token(identity=username)
			refresh_token = create_refresh_token(identity=username)
			ret = {'access_token': access_token}
			resp = redirect(url_for('store.list_items'))
			set_access_cookies(resp, access_token)
			set_refresh_cookies(resp, refresh_token)

			return resp

	return jsonify({"msg": "Bad username or password"}), 401
	

# Because the JWTs are stored in an httponly cookie now, we cannot
# log the user out by simply deleting the cookie in the frontend.
# We need the backend to send us a response to delete the cookies
# in order to logout. unset_jwt_cookies is a helper function to
# do just that.
@app.route('/logout', methods=['GET'])
@jwt_required
def logout():
    resp = redirect(url_for('index.landing'))
    unset_jwt_cookies(resp)
    return resp


# Protect a view with jwt_required, which requires a valid access token
# in the request to access.
@app.route('/protected', methods=['GET'])
@jwt_required
def protected():
	# Access the identity of the current user with get_jwt_identity
	current_user = get_jwt_identity()
	return jsonify({'current_user': current_user}), 200


if __name__ == '__main__':
	app.run(port=5001)
