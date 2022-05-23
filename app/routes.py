import json
from flask import request, render_template, redirect, flash, url_for, session

from app import app
from app.models import athlete_show_fields, athlete_search_fields, achievment_fields
from app.db_operator import mongo_operator, elastic_operator
from app.loader import read_file
from app.validate import validate_insert, validate_update, validate_delete


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
        athlete_show_fields=athlete_show_fields,
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
        athlete_show_fields=athlete_show_fields,
        achievment_fields=achievment_fields
    )


@app.route("/forms")
def forms():
    sample_insert = read_file("samples/sample_insert.json")
    sample_update = read_file("samples/sample_update.json")
    sample_delete = read_file("samples/sample_delete.json")

    if session.get("message"):
        flash(session["message"])
        session.pop("message")

    return render_template(
        "forms.html",
        athlete_show_fields=athlete_show_fields,
        achievment_fields=achievment_fields,
        sample_insert=sample_insert,
        sample_update=sample_update,
        sample_delete=sample_delete,
    )


@app.route("/insert", methods=["POST"])
def insert_from_web():
    valid, message = validate_insert(request.json["editor-insert"])
    
    if valid:
        json_data = json.loads(request.json["editor-insert"])
        elastic_operator.common_insert(json_data)
        mongo_operator.common_insert(json_data)

    session["message"] = message
    return "None"


@app.route("/update", methods=["POST"])
def update_from_web():
    valid, message = validate_update(request.json["editor-update"])

    if valid:
        json_data = json.loads(request.json["editor-update"])
        elastic_operator.common_update(
            query=json_data["query"], 
            update=json_data["update"], 
            how=json_data["how"]
        )
        mongo_operator.common_update(
            filters=json_data["query"], 
            update=json_data["update"], 
            how=json_data["how"]
        )

    session["message"] = message
    return "None"


@app.route("/delete", methods=["POST"])
def delete_from_web():
    valid, message = validate_delete(request.json["editor-delete"])

    if valid:
        json_data = json.loads(request.json["editor-delete"])
        elastic_operator.common_delete(
            query=json_data["query"], 
            how=json_data["how"]
        )
        mongo_operator.common_delete(
            filters=json_data["query"], 
            how=json_data["how"]
        )

    session["message"] = message
    return "None"