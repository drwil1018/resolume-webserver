from flask import Flask
from flask_cors import CORS

base_url = "http://localhost:8080/api/v1"

app = Flask(__name__)
CORS(app)