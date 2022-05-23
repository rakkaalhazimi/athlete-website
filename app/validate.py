import json
from app.db_operator import mongo_operator, elastic_operator
from app.models import athlete_fields


def jsonable_text(text):
    try:
        json_data = json.loads(text)
        status = True
    except json.decoder.JSONDecodeError:
        json_data = None
        status = False
    return json_data, status


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


def data_model_check(json_data):
    athlete_keys = set(athlete_fields)
    current_keys = set(json_data.keys())
    outlier_keys = current_keys.difference(athlete_keys)
    if not outlier_keys:
        return True, outlier_keys
    else:
        return False, outlier_keys


def validate_insert(text):
    message = "Data Inserted"
    
    # JSON Format Check
    json_data, jsonable = jsonable_text(text)
    if not jsonable:
        message = "The text have a wrong json format"
        return False, message
    
    # Duplicate Athlete_ID Check
    not_duplicate = non_duplicate_id(json_data)
    if not not_duplicate:
        message = "Duplicate Athlete_ID, please use different numbers"
        return False, message

    return True, message


def validate_update(text):
    message = "Data Updated"
    
    # JSON Format Check
    json_data, jsonable = jsonable_text(text)
    if not jsonable:
        message = "The text have a wrong json format"
        return False, message

    query, update = json_data["query"], json_data["update"]

    # Duplicate Athlete_ID Check
    if "Athlete_ID" in update.keys():
        not_duplicate = non_duplicate_id(update)
        if not not_duplicate:
            message = "Duplicate Athlete_ID, please use different numbers"
            return False, message

    return True, message


def validate_delete(text):
    message = "Data Deleted"
    
    # JSON Format Check
    json_data, jsonable = jsonable_text(text)
    if not jsonable:
        message = "The text have a wrong json format"
        return False, message

    return True, message