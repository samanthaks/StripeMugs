import boto3
import json
import logging
import os

from flask import Flask
from flask_cors import CORS, cross_origin
from flask.ext.assets import Environment, Bundle

application = None
assets = None
db = None


def create_app():
    global app
    global assets
    global db

    application = Flask(__name__)
    app.config.from_object('config.dev')

    assets = Environment(application)
    register_keys()
    register_scss()
    db = register_db(app)

    CORS(application)

    return application

def register_db(application):
    app = application
    boto_session = boto3.session.Session(aws_access_key_id=app.config['AWS_ACCESS_KEY_ID'],
            aws_secret_access_key=app.config['AWS_SECRET_ACCESS_KEY'])
    db = boto_session.resource('dynamodb',region_name='us-west-2')
    return db

def register_keys():
    os.environ['SECRET_KEY'] = application.config['STRIPE_SECRET_KEY']
    os.environ['PUBLISHABLE_KEY'] = application.config['STRIPE_PUBLISHABLE_KEY']

def register_scss():
    assets.url = application.static_url_path
    with open(application.config['SCSS_CONFIG_FILE']) as f:
        bundle_set = json.loads(f.read())
        output_folder = bundle_set['output_folder']
        depends = bundle_set['depends']
        for bundle_name, instructions in bundle_set['rules'].iteritems():
            bundle = Bundle(*instructions['inputs'],
                            output=output_folder + instructions['output'],
                            depends=depends,
                            filters='scss')
            assets.register(bundle_name, bundle)
