#!/usr/bin/python3
""" configuration """

from models import storage
from api.v1.views import app_views
from os import getenv
from flask import Flask, make_response, jsonify

# flask app
app = Flask(__name__)

# register blueprint
app.register_blueprint(app_views)

# method to handle app
@app.teardown_appcontext
def close_storage(exception):
    storage.close()

# Run  Flask server
if __name__ == "__main__":
    
    # Set host and port
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(getenv('HBNB_API_PORT', 5000))

    # Run the Flask server
    app.run(host=host, port=port, threaded=True)
