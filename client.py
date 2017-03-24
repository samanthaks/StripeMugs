from flask import render_template, redirect
from client import create_app

app = create_app()

@app.route('/', methods=['GET'])
def landing():
	return render_template('index.html')

@app.route('/storeItem', methods=['GET'])
def test():
	# 
	# use this json to render storeItem page
	return redirect("https://i9p6a7vjqf.execute-api.us-west-2.amazonaws.com/prod/apps/catalog/2")

@app.route('/accounts', methods=['GET'])
	# account
	return redirect("https://i9p6a7vjqf.execute-api.us-west-2.amazonaws.com/prod/apps/accounts/{id}")

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
# 	   Item={
# 	        'trans_id': count + 1,
# 	        'customer': customer.id,
# 	        'email': request.form['stripeEmail'],
# 	        'amount': amount,
# 	        'date': i.strftime('%Y/%m/%d %H:%M:%S'),
# 	        'item_id': request.form['item_id']
# 	    }
# 	)

#     return render_template('charges.html', amount=amount)



if __name__ == "__main__":
    app.run(port=5000)
