from flask import render_template, request, url_for
from client import create_app
import requests


app = create_app()

STORE_URL="http://127.0.0.1:5002/store"

@app.route('/', methods=['GET'])
def landing():
	items_dict = url_for('store.list_items')
	return render_template('store.html', storeItems=items_dict['Items'], key=app.config['STRIPE_TEST_PUBLISHABLE_KEY'])
	# return render_template('index.html')

if __name__ == "__main__":
    app.run(port=5000)
