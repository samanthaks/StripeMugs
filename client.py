from flask import render_template
from client import create_app

app = create_app()

@app.route('/', methods=['GET'])
def landing():
	return render_template('index.html')

if __name__ == "__main__":
    app.run(port=5000)
