from flask import request, render_template, flash
from app import app, mongo_client, elastic_client
from app.models import athlete_fields, athlete_search_fields, achievment_fields
from app.db_operator import MongodbOperator, ElasticOperator


mongo_operator = MongodbOperator(mongo_client)
elastic_operator = ElasticOperator(elastic_client)


@app.route("/", methods=["GET"])
def home():
    # Fetch user queries
    queries = {}
    for field in athlete_search_fields:
        value = request.args.get(field, None)
        if value not in [None, ""]:
            queries[field] = value

    # Check if any user has query
    is_query = any(queries.values())
    if not is_query:
        athletes_data = mongo_operator.search_operation()
    else:
        filters = queries
        documents, elapsed = elastic_operator.search_operation(filters)
        print(documents, elapsed)
        athletes_data = mongo_operator.search_operation(filters=filters)

    
    return render_template(
        "index.html", 
        athlete_fields=athlete_fields,
        athlete_search_fields=athlete_search_fields,
        athletes_data=athletes_data
    )