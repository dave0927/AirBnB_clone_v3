#!/usr/bin/python3
"""
    Entry into flask application
"""

from flask import Flask, jsonify
from flask_cors import CORS
from models import storage
from api.v1.views import app_views
import os

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def close_storage(error):
    """Closes the storage engine on teardown."""
    storage.close()


@app.errorhandler(404)
def page_not_found(e):
    """
        Handler that returns a JSON-formatted 404
        status code response
    """
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = os.getenv('HBNB_API_PORT', '5000')
    app.run(host=host, port=port, threaded=True)
