from flask import Flask
from flask_cors import CORS
import os

# Use host.docker.internal instead of localhost when running in Docker
# This allows the container to connect to services on the host machine
base_url = "http://192.168.8.178:8080/api/v1"

app = Flask(__name__)
CORS(app)
