import json
import logging
import os

from flask import Flask
from flask.ext.assets import Environment, Bundle


app = None
assets = None


def create_app(**config_overrides):
    global app
    global assets
    app = Flask(__name__)

    app.config.from_object('config.dev')
    app.config.update(config_overrides)

    assets = Environment(app)
    register_keys()
    register_scss()
    register_blueprints(app)
    register_logger(app)
    

    return app


def register_keys():
    os.environ['SECRET_KEY'] = app.config['STRIPE_SECRET_KEY']
    os.environ['PUBLISHABLE_KEY'] = app.config['STRIPE_PUBLISHABLE_KEY']


def register_logger(app):
    """Create an error logger and attach it to ``app``."""

    max_bytes = int(app.config["LOG_FILE_MAX_SIZE"]) * 1024 * 1024   # MB to B
    # Use "# noqa" to silence flake8 warnings for creating a variable that is
    # uppercase.  (Here, we make a class, so uppercase is correct.)
    Handler = logging.handlers.RotatingFileHandler  # noqa
    f_str = ('%(levelname)s @ %(asctime)s @ %(filename)s '
             '%(funcName)s %(lineno)d: %(message)s')

    access_handler = Handler(app.config["WERKZEUG_LOG_NAME"],
                             maxBytes=max_bytes)
    access_handler.setLevel(logging.INFO)
    logging.getLogger("werkzeug").addHandler(access_handler)

    app_handler = Handler(app.config["APP_LOG_NAME"], maxBytes=max_bytes)
    formatter = logging.Formatter(f_str)
    app_handler.setLevel(logging.INFO)
    app_handler.setFormatter(formatter)
    app.logger.addHandler(app_handler)

def register_blueprints(app):
    from app.routes import client
    from app.routes import payment
    app.register_blueprint(client)
    app.register_blueprint(payment)

def register_scss():
    assets.url = app.static_url_path
    with open(app.config['SCSS_CONFIG_FILE']) as f:
        bundle_set = json.loads(f.read())
        output_folder = bundle_set['output_folder']
        depends = bundle_set['depends']
        for bundle_name, instructions in bundle_set['rules'].iteritems():
            bundle = Bundle(*instructions['inputs'],
                            output=output_folder + instructions['output'],
                            depends=depends,
                            filters='scss')
            assets.register(bundle_name, bundle)
