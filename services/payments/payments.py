from flask import Flask


app = Flask(__name__)

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

if __name__ == '__main__':
	app.run(port=5004)
