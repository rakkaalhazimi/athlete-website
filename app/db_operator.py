from typing import List, Dict
from app.db_client import DBClient


# Mongodb operations
# ==================
def get_mongo_query_search(filters: Dict):
    query_search = dict(filters)
    patterns = [f".*{value}.*" for value in filters.values()]
    regex_query = [{"$regex": pattern, "$options": "i"} for pattern in patterns]
    for field, query in zip(query_search.keys(), regex_query):
        query_search[field] = query
    return query_search

def get_mongo_elapsed(search_result):
    return search_result.explain()["executionStats"]["executionTimeMillis"]


class MongodbOperator:
    def __init__(self, client: DBClient):
        self.client = client

    def common_search(self):
        search_result = self.client.search_data()
        elapsed = get_mongo_elapsed(search_result)
        return search_result, elapsed

    def query_search(self, filters: Dict):
        query = get_mongo_query_search(filters)
        search_result = self.client.search_data(filters=query)
        elapsed = get_mongo_elapsed(search_result)
        return search_result, elapsed


# Elasticsearch operations
# ========================
def get_elastic_query_search(filters: Dict):
    fields = list(filters.keys())
    query = [f"*{value}*" for value in filters.values()]
    query = " AND ".join(query)
    query_search = {
        "query_string": {
            "fields": fields, 
            "query": query
        }
    }
    return query_search

def parse_elastic_results(search_result):
    documents = search_result["hits"]["hits"]
    if documents:
        documents = [doc["_source"] for doc in documents]
    elapsed = search_result["took"]
    return documents, elapsed


class ElasticOperator:
    def __init__(self, client: DBClient):
        self.client = client

    def common_search(self):
        search_result = self.client.search_data()
        documents, elapsed = parse_elastic_results(search_result)
        print(documents)
        return documents, elapsed
    
    def query_search(self, filters: Dict):
        query = get_elastic_query_search(filters)
        search_result = self.client.search_data(query=query)
        documents, elapsed = parse_elastic_results(search_result)
        return documents, elapsed