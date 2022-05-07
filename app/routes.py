from flask import request, render_template
from app import app, mongo_client, elastic_client

@app.route("/", methods=["GET"])
def home():
    query = request.args.get("query")
    if not query:
        athletes = mongo_client.search_data()
    else:
        filters = {"Athlete_Name": query}
        athletes = mongo_client.search_data(filters=filters)
    
    return render_template("index.html", athletes=athletes)