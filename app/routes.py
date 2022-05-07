from flask import request, render_template
from app import app

@app.route("/", methods=["GET"])
def home():
    if request.method == "GET":
        athletes = ["Maradona", "Leon"]
        return render_template("index.html", athletes=athletes)