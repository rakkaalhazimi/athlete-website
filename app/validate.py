import json
from flask import flash
from app.db_operator import mongo_operator, elastic_operator


def jsonable(text):
    return json.loads(text)


def non_duplicate_id(query):
    athlete_id = query["Athlete_ID"]
    search_query = {"Athlete_ID": athlete_id}
    
    mongo_documents, _ = mongo_operator.common_search(search_query)
    elastic_documents, _ = elastic_operator.common_search(search_query)
    
    len_mongo = len([doc for doc in mongo_documents])
    len_elastic = len(elastic_documents)
    
    # Return True if there is no duplicate, else False
    if len_mongo + len_elastic == 0:
        return True
    else:
        return False


def validate_insert(text):
    json_data = jsonable(text)
    if not non_duplicate_id(json_data):
        flash("Duplicate Athlete_ID, please use different numbers")
        print("Failed")
    return json_data
