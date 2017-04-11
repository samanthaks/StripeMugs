from flask import Flask, jsonify, request, Blueprint, redirect, url_for, session
from flask_jwt_extended import JWTManager, jwt_required,\
	create_access_token, get_jwt_identity, set_access_cookies, create_refresh_token, set_refresh_cookies, unset_jwt_cookies
import boto3
from boto3.dynamodb.conditions import Key, Attr

CUSTOMER_URL = 'https://i9p6a7vjqf.execute-api.us-west-2.amazonaws.com/prod/apps/customers'

app = Flask(__name__)
app.config.from_object('config')
boto_session = boto3.session.Session(aws_access_key_id=app.config['AWS_ACCESS_KEY_ID'], aws_secret_access_key=app.config['AWS_SECRET_ACCESS_KEY'])
db = boto_session.resource('dynamodb',region_name='us-west-2') #not sure if needed here?



# this will hit an API endpoint that should trigger an AWS step function, which will take the email,
# hit a verification API, and if all goes well, create an entry in the 'Customers' table
# and then the Lambda function will ultimately return some sort of status message here.

@app.route('/join', methods=['POST']) # methods that this route will respond to
def createCustomer():
	request_body = {}
	request_body['username'] = request.form['username']
	request_body['email'] = request.form['email']
	request_body['password'] = request.form['password']

	# need to wrap the above into a JWT for security purposes?

	#send a POST request to API endpoint with username, email, password as the POST body.
	# will be body-mapped into the Lambda function's event object and inserted into Dynamo from there.
	res = requests.post(CUSTOMER_URL, json=request_body)
	print 'response from server: ' + res.text
	response_dict = res.json()
	# need to write business logic for handling email verification failure case
	return response_dict # for now









if __name__ == '__main__':
	app.run(port=5003)
