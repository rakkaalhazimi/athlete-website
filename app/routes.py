from flask import request, render_template, flash
from app import app, mongo_client, elastic_client
from app.models import athlete_fields, athlete_search_fields, achievment_fields
from app.db_operator import MongodbOperator, ElasticOperator


database = {
    "MongoDB": MongodbOperator(mongo_client), 
    "ElasticSearch": ElasticOperator(elastic_client)
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
        print(athletes_data, elapsed)

    
    return render_template(
        "index.html", 
        athlete_fields=athlete_fields,
        athlete_search_fields=athlete_search_fields,
        athletes_data=athletes_data
    )