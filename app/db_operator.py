from typing import List, Dict
from app import mongo_client, elastic_client
from app.db_client import DBClient
from app.query import (
    MongodbQueryBuilder,
    MongodbQueryGetter,
    EsQueryBuilder,
    EsQueryGetter,
)


# Mongodb operations
# ==================
class MongodbOperator:
    def __init__(self, client: DBClient):
        self.client = client
        self.query_builder = MongodbQueryBuilder()
        self.query_getter = MongodbQueryGetter()

    def common_search(self, filters: Dict = {}):
        search_result = self.client.search_data(filters=filters)
        elapsed = self.query_getter.get_mongo_elapsed(search_result)
        return search_result, elapsed

    def query_search(self, filters: Dict):
        query = self.query_builder.create_mongo_regex_search(filters)
        search_result = self.client.search_data(filters=query)
        elapsed = self.query_getter.get_mongo_elapsed(search_result)
        return search_result, elapsed

    def common_update(self, filters: Dict, update: Dict, how: str = "one"):
        update_query = self.query_builder.create_mongo_update_query(update)
        update_result = self.client.update_data(
            filters=filters, update=update_query, how=how
        )
        return update_result


# Elasticsearch operations
# ========================
class ElasticOperator:
    def __init__(self, client: DBClient):
        self.client = client
        self.query_builder = EsQueryBuilder()
        self.query_getter = EsQueryGetter()

    def common_search(self, filters: Dict = None):
        search_result = self.client.search_data(filters)
        documents = self.query_getter.get_documents_results(search_result)
        elapsed = self.query_getter.get_elastic_elapsed(search_result)
        return documents, elapsed

    def query_search(self, filters: Dict):
        query = self.query_builder.create_elastic_query_search(filters)
        search_result = self.client.search_data(query=query)
        documents = self.query_getter.get_documents_results(search_result)
        elapsed = self.query_getter.get_elastic_elapsed(search_result)
        return documents, elapsed

    def common_update(self, filters: Dict, update: Dict, how: str = "one"):
        update_filter = self.query_builder.create_elastic_match_query(filters)
        update_result = self.client.update_data(
            query=update_filter, update=update, how=how
        )
        elapsed = self.query_getter.get_elastic_elapsed(update_result)
        return update_result, elapsed


mongo_operator = MongodbOperator(mongo_client)
elastic_operator = ElasticOperator(elastic_client)
