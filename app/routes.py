from app import app, base_url
from flask import render_template, flash
import requests

@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html", title="Home")

@app.route("/balls", methods=["GET", "POST"])
def balls():
    response = requests.post(f"{base_url}/composition/columns/1/connect")
    if response.status_code != 204:
        flash("ERROR")


    return render_template("balls.html")
    

