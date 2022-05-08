from flask import request, render_template
from app import app, mongo_client, elastic_client
from app.models import athlete_fields, athlete_search_fields, achievment_fields


@app.route("/", methods=["GET"])
def home():
    query = request.args.get("Athlete_Name")
    if not query:
        athletes_data = mongo_client.search_data()
    else:
        filters = {"Athlete_Name": query}
        athletes_data = mongo_client.search_data(filters=filters)
    
    return render_template(
        "index.html", 
        athlete_fields=athlete_fields,
        athlete_search_fields=athlete_search_fields,
        athletes_data=athletes_data
    )