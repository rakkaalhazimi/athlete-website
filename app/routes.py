from flask import request, render_template, flash
from app import app
from app.models import athlete_fields, athlete_search_fields, achievment_fields
from app.db_operator import mongo_operator, elastic_operator


database = {
    "MongoDB": mongo_operator, 
    "ElasticSearch": elastic_operator
}


@app.route("/", methods=["GET"])
def home():
    # Fetch user queries
    queries = {}
    for field in athlete_search_fields:
        value = request.args.get(field, None)
        if value not in [None, ""]:
            queries[field] = value

    # Choose DB
    db_choice = request.args.get("database")
    db_operator = database.get(db_choice) or database.get("MongoDB")

    # Check if any user has query
    is_query = any(queries.values())

    if not is_query:
        athletes_data, elapsed = db_operator.common_search()
    else:
        filters = queries
        athletes_data, elapsed = db_operator.query_search(filters)
    
    return render_template(
        "index.html", 
        athlete_fields=athlete_fields,
        athlete_search_fields=athlete_search_fields,
        athletes_data=athletes_data,
        elapsed=elapsed
    )


@app.route("/<int:athlete_id>")
def info(athlete_id):
    # Database common search
    athlete_info, elapsed = database["MongoDB"].common_search({"Athlete_ID": athlete_id})
    
    # Retrieve data from search results
    athlete_info = next(athlete_info)

    return render_template(
        "info.html", 
        athlete_info=athlete_info,
        athlete_fields=athlete_fields,
        achievment_fields=achievment_fields
    )


@app.route("/forms")
def forms():
    return render_template("forms.html")