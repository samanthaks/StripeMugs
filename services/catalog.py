from flask import Flask, session, redirect, url_for, render_template, request, jsonify, Response, flash, Blueprint, session
import requests
import json
from flask_jwt_extended import JWTManager, jwt_required
import os
import stripe
import boto3
from datetime import datetime


app = Flask(__name__)
# app.config.from_object('config.dev')
boto_session = boto3.session.Session(aws_access_key_id=app.config['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=app.config['AWS_SECRET_ACCESS_KEY'])
db = boto_session.resource('dynamodb',region_name='us-west-2')


stripe_keys = {
  'secret_key': os.environ['SECRET_KEY'],
  'publishable_key': os.environ['PUBLISHABLE_KEY']
}

stripe.api_key = stripe_keys['secret_key']


@app.route('/store', methods=['GET'])
@jwt_required
def list_items():
	items_dict = db.Table('items').scan()
	return render_template('store.html', storeItems=items_dict['Items'], key=stripe_keys['publishable_key'])


@app.route('/charge', methods=['POST'])
def charge():

    amount = int(request.form['amount'])
    count = int(db.Table('Transactions').scan()['Count'])

    customer = stripe.Customer.create(
        email=request.form['stripeEmail'],
        source=request.form['stripeToken']
    )

    charge = stripe.Charge.create(
        customer=customer.id,
        amount=amount*100,
        currency='usd',
        description='Flask Charge',
        metadata={'order_id': count+1}
    )

    i = datetime.now()
    response = db.Table('Transactions').put_item(
	   Item={
	        'trans_id': count + 1,
	        'customer': customer.id,
	        'email': request.form['stripeEmail'],
	        'amount': amount,
	        'date': i.strftime('%Y/%m/%d %H:%M:%S'),
	        'item_id': request.form['item_id']
	    }
	)

    return render_template('charges.html', amount=amount)


if __name__ == "__main__":
    app.run(port=5002, instance_relative_config=True)
