#!/usr/bin/python3
""" configuration """

from models import storage
from api.v1.views import app_views
from os import getenv
from flask import Flask, make_response, jsonify
from flask_cors import CORS

# flask app
app = Flask(__name__)

# register blueprint
app.register_blueprint(app_views)

# Create CORS instance allowing /* for 0.0.0.0
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def close_storage(exception):
    """ close method"""
    storage.close()

# Handler for 404 errors


@app.errorhandler(404)
def not_found(error):
    """ 404 error method"""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    # Set host and port
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(getenv('HBNB_API_PORT', 5000))

    # Run the Flask server
    app.run(host=host, port=port, threaded=True)
