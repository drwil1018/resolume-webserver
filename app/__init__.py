from flask import Flask

app = Flask(__name__)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

base_url = "http://localhost:8080/api/v1"

from app import routes