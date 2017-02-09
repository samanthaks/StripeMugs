from flask import session, redirect, url_for, render_template, request, jsonify, Response, flash, Blueprint, session
import requests
import json
from flask_jwt_extended import JWTManager, jwt_required
from .. import db
import os
import stripe


store = Blueprint('store', __name__)

stripe_keys = {
  'secret_key': os.environ['SECRET_KEY'],
  'publishable_key': os.environ['PUBLISHABLE_KEY']
}

stripe.api_key = stripe_keys['secret_key']


@store.route('/store', methods=['GET'])
@jwt_required
def list_items():
	items_dict = db.Table('items').scan()
	return render_template('store.html', storeItems=items_dict['Items'], key=stripe_keys['publishable_key'])


@store.route('/charge', methods=['POST'])
def charge():
    # Amount in cents
    amount = 500

    customer = stripe.Customer.create(
        email='customer@example.com',
        source=request.form['stripeToken']
    )

    charge = stripe.Charge.create(
        customer=customer.id,
        amount=amount,
        currency='usd',
        description='Flask Charge'
    )

    return render_template('charge.html', amount=amount)

