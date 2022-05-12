from typing import List, Dict
from app.db_client import DBClient


# Mongodb operations
# ==================
def get_mongo_query_search(filters: Dict):
    """
    Build mongoDB query search from specified filters.
    
    example:
      input <- {"name": "aji"}
      output <- {"$regex": {"name": ".*aji.*"}, "$options": "i" }

    """
    query_search = dict(filters)
    patterns = [f".*{value}.*" for value in filters.values()]
    regex_query = [{"$regex": pattern, "$options": "i"} for pattern in patterns]
    
    for field, query in zip(query_search.keys(), regex_query):
        query_search[field] = query

    return query_search


def get_mongo_elapsed(result):
    return result.explain()["executionStats"]["executionTimeMillis"]


def create_mongo_update_query(update):
    update_query = {"$set": update}
    return update_query


class MongodbOperator:
    def __init__(self, client: DBClient):
        self.client = client

    def common_search(self, filters: Dict = {}):
        search_result = self.client.search_data(filters=filters)
        elapsed = get_mongo_elapsed(search_result)
        return search_result, elapsed

    def query_search(self, filters: Dict):
        query = get_mongo_query_search(filters)
        search_result = self.client.search_data(filters=query)
        elapsed = get_mongo_elapsed(search_result)
        return search_result, elapsed

    def common_update(self, filters: Dict, update: Dict, how: str):
        update_query = create_mongo_update_query(update)
        update_result = self.client.update_data(filters=filters, update=update_query, how=how)
        return update_result


# Elasticsearch operations
# ========================
def get_elastic_query_search(filters: Dict):
    """
    Build ElasticSearch query search from specified filters.
    
    example:
      input <- {"name": "aji"}
      output <- {"query_string": {"fields": "name", "query": "*aji*"}}
      
    """
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
    """
    Parse ElasticSearch search results.
    
    The search results came with this format: 
      {..., hits: {..., hits: ..., _source:}}
    
    The data lies inside _source keys, therefore we need
    to access it.
      
    """
    documents = search_result["hits"]["hits"]
    if documents:
        documents = [doc["_source"] for doc in documents]
    return documents


def get_elastic_elapsed(result):
    return result["took"]


class ElasticOperator:
    def __init__(self, client: DBClient):
        self.client = client

    def common_search(self, filters: Dict = None):
        search_result = self.client.search_data(filters)
        documents = parse_elastic_results(search_result)
        elapsed = get_elastic_elapsed(search_result)
        return documents, elapsed
    
    def query_search(self, filters: Dict):
        query = get_elastic_query_search(filters)
        search_result = self.client.search_data(query=query)
        documents = parse_elastic_results(search_result)
        elapsed = get_elastic_elapsed(search_result)
        return documents, elapsed