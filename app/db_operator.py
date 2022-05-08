from typing import List, Dict
from app.db_client import DBClient


# Mongodb operations
# ==================
class MongodbOperator:
    def __init__(self, client: DBClient):
        self.client = client

    def search_operation(self, filters: Dict):
        search_result = self.client.search_data(filters=filters)
        return search_result


# Elasticsearch operations
# ========================
def get_elastic_query_string(filters: Dict):
    fields = list(filters.keys())
    query = [f"*{value}*" for value in filters.values()]
    query = " AND ".join(query)
    query_string = {
        "query_string": {
            "fields": fields, 
            "query": query
        }
    }
    return query_string

def parse_elastic_results(search_result):
    documents = search_result["hits"]["hits"]
    if documents:
        documents = [doc["_source"] for doc in documents]
    elapsed = search_result["took"]
    return documents, elapsed


class ElasticOperator:
    def __init__(self, client: DBClient):
        self.client = client

    def search_operation(self, filters: Dict):
        query = get_elastic_query_string(filters)
        search_result = self.client.search_data(query=query)
        documents, elapsed = parse_elastic_results(search_result)
        return documents, elapsed