import os
from flask import Flask
from routes import pages
from pymongo import MongoClient
from dotenv import load_dotenv
import time

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.register_blueprint(pages)
    print(os.environ.get("MONGODB_URI"))
    client = MongoClient(os.environ.get("MONGODB_URI"))
    app.db = client.get_database("completions")
    return app
