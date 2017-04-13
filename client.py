from flask import render_template, redirect, request, jsonify, json, url_for
from client import create_app
import requests
import os

app = create_app()

ACCOUNTS_URL="https://i9p6a7vjqf.execute-api.us-west-2.amazonaws.com/prod/apps/accounts/"
# ACCOUNTS_URL="https://i9p6a7vjqf.execute-api.us-west-2.amazonaws.com/prod/apps/accounts/test@test.com"

CATALOGUE_URL="https://i9p6a7vjqf.execute-api.us-west-2.amazonaws.com/prod/apps/catalog"
stripe_keys = {
  'secret_key': os.environ['SECRET_KEY'],
  'publishable_key': os.environ['PUBLISHABLE_KEY']
}

# stripe.api_key = stripe_keys['secret_key']
@app.route('/', methods=['GET'])
def landing():
  return render_template('index.html')


@app.route('/login', methods=['POST'])
def login():
  LOGIN_URL = 'https://i9p6a7vjqf.execute-api.us-west-2.amazonaws.com/prod/apps/customers/'
  params = {
  	'username': request.form.get('username'),
  	'password': request.form.get('password')
  }
  r = requests.get(LOGIN_URL, params=params)
  print(r.url)
  print(r.json())
  if 'Item' in r.json()['body']:
  	# Success
  	return redirect(url_for('store'))
  else:
  	# Fail
  	return redirect(url_for('landing'))


@app.route('/charge', methods=['GET'])
def getCharge():
  # print "RECEIVED CHARGE!"
  amount = int(request.args.get('amount'))
  return render_template("charges.html", amount=amount)

@app.route('/transactions', methods=["GET"])
def getTransactions():
    ACCOUNTS_URL="https://i9p6a7vjqf.execute-api.us-west-2.amazonaws.com/prod/apps/payments/"

    account_email = request.args.get('email')
    transactions_list = requests.get(ACCOUNTS_URL).json()
    # print transactions_list
    transactions = []

    #only the transactions for this user
    for t in transactions_list:
      if t["email"] == account_email:
        transactions.append(t)

    return render_template("transactions.html", transactions=transactions)

  # link to user's tranactions / email / name
@app.route('/storeItem', methods=['GET'])
def store():
  #
  # use this json to render storeItem page
  response = requests.get(CATALOGUE_URL).json()

  # The email shouldd be from the user info that is logged in
  email = "test@test.com"

  # items_dict = jsonify(json.loads(response.text))
  items_dict = response
  # items_dict = {}
  # items_dict['price'] = str(response['price']).encode('utf-8')
  # items_dict['itemName'] = str(response['itemName'])
  # items_dict['imgUrl'] = str(response['imgUrl'])
  # items_dict['description'] = str(response['description'])
  # items_dict['id'] = str(response['id'])

  # print items_dict
  # print "STRIPE KEYS {}".format(stripe_keys)

  return render_template('store.html', storeItems=items_dict, key=stripe_keys['publishable_key'], email=email)

  # return redirect("https://i9p6a7vjqf.execute-api.us-west-2.amazonaws.com/prod/apps/catalog/2")

# @app.route('/accounts', methods=['GET'])
# def getAccounts():
#   request = requests.get(ACCOUNTS_URL)
#   print json.dumps(request.json)
#   items_dict = json.dumps(request.json)
#   # return render_template()
#   return render_template('store.html', storeItems=items_dict['Items'], key=stripe_keys['publishable_key'])


# customer
# https://i9p6a7vjqf.execute-api.us-west-2.amazonaws.com/prod/apps/customers/{id}

# payment
# https://i9p6a7vjqf.execute-api.us-west-2.amazonaws.com/prod/apps/payments/{id}

# @app.route('/charge', methods=['POST'])
# def charge():

#     amount = int(request.form['amount'])
#     count = int(db.Table('Transactions').scan()['Count'])

#     customer = stripe.Customer.create(
#         email=request.form['stripeEmail'],
#         source=request.form['stripeToken']
#     )

#     charge = stripe.Charge.create(
#         customer=customer.id,
#         amount=amount*100,
#         currency='usd',
#         description='Flask Charge',
#         metadata={'order_id': count+1}
#     )

#     i = datetime.now()
#     response = db.Table('Transactions').put_item(
#      Item={
#           'trans_id': count + 1,
#           'customer': customer.id,
#           'email': request.form['stripeEmail'],
#           'amount': amount,
#           'date': i.strftime('%Y/%m/%d %H:%M:%S'),
#           'item_id': request.form['item_id']
#       }
#   )

#     return render_template('charges.html', amount=amount)



if __name__ == "__main__":
    app.run(port=8080)
