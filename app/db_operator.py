from typing import List, Dict
from app import mongo_client, elastic_client
from app.db_client import DBClient
from app.query import (
    MongodbQueryBuilder,
    MongodbQueryGetter,
    EsQueryBuilder,
    EsQueryGetter,
)
from app.perf import CodeTimer

timer = CodeTimer()


# Mongodb operations
# ==================
class MongodbOperator:
    """
    A concrete class to manage different queries needed for MongoDB Client operation.
    """
    def __init__(self, client: DBClient):
        self.client = client
        self.query_builder = MongodbQueryBuilder()
        self.query_getter = MongodbQueryGetter()
    
    def common_insert(self, data: List[Dict]):
        """
        MongoDB common insert data operator.

        flow:
        json_data -> database -> insert_result
                              -> elapsed

        return:
          insert_result: MongoDB insert result
          elapsed: time used to insert data to MongoDB
        
        """
        with timer as runtime:
            insert_result = self.client.insert_data(data)
        elapsed = runtime.value
        return insert_result, elapsed

    def common_search(self, filters: Dict = {}):
        """
        MongoDB common search data operator.

        flow:
        json_data -> search_query -> database -> search_result -> documents
                                                               -> elapsed

        return:
          documents: MongoDB search result's documents
          elapsed: time used to search data in MongoDB
        
        """
        search_result = self.client.search_data(filters=filters)
        elapsed = self.query_getter.get_mongo_elapsed(search_result)
        return search_result, elapsed

    def query_search(self, filters: Dict):
        """
        MongoDB regex string search data operator.

        flow:
        json_data -> search_query -> database -> search_result -> documents
                                                               -> elapsed

        return:
          documents: MongoDB search result's documents
          elapsed: time used to search data in MongoDB
        
        """
        query = self.query_builder.create_mongo_regex_search(filters)
        search_result = self.client.search_data(filters=query)
        elapsed = self.query_getter.get_mongo_elapsed(search_result)
        return search_result, elapsed

    def common_update(self, filters: Dict, update: Dict, how: str = "one"):
        """
        MongoDB common update data operator.

        flow:
        json_data -> search_query -> database -> update_result
                     update_query             -> elapsed
                     how

        return:
          update_result: MongoDB update result
          elapsed: time used to update data in MongoDB
        
        """
        update_query = self.query_builder.create_mongo_update_query(update)
        with timer as runtime:
            update_result = self.client.update_data(
                filters=filters, update=update_query, how=how
            )
        elapsed = runtime.value
        return update_result, elapsed

    def common_delete(self, filters: Dict, how: str = "one"):
        """
        MongoDB common delete data operator.

        flow:
        json_data -> search_query -> database -> delete_result
                     how                      -> elapsed

        return:
          delete_result: MongoDB delete result
          elapsed: time used to delete data in MongoDB
        
        """
        with timer as runtime:
            update_result = self.client.delete_data(
                filters=filters, how=how
            )
        elapsed = runtime.value
        return update_result, elapsed


# Elasticsearch operations
# ========================
class ElasticOperator:
    """
    A concrete class to manage different queries needed for ElasticSearch Client operation.
    """
    def __init__(self, client: DBClient):
        self.client = client
        self.query_builder = EsQueryBuilder()
        self.query_getter = EsQueryGetter()

    def common_insert(self, data: List[Dict]):
        """
        ElasticSearch common insert data operator.

        flow:
        json_data -> database -> insert_result
                              -> elapsed

        return:
          insert_result: ElasticSearch insert result
          elapsed: time used to insert data to ElasticSearch
        
        """
        with timer as runtime:
            insert_result = self.client.insert_data(data)
        elapsed = runtime.value
        return insert_result, elapsed

    def common_search(self, query: Dict = None):
        """
        ElasticSearch common search data operator.
        It is a search using match format in:
        https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-match-query.html

        flow:
        json_data -> search_query -> database -> search_result -> documents
                                                               -> elapsed

        return:
          documents: ElasticSearch search result's documents
          elapsed: time used to search data in ElasticSearch
        
        """
        search_query = query

        if query:
            search_query = self.query_builder.create_elastic_match_query(query)

        search_result = self.client.search_data(search_query)
        documents = self.query_getter.get_documents_results(search_result)
        elapsed = self.query_getter.get_elastic_elapsed(search_result)
        return documents, elapsed

    def query_search(self, query: Dict):
        """
        ElasticSearch query string search data operator.

        flow:
        json_data -> search_query -> database -> search_result -> documents
                                                               -> elapsed

        return:
          documents: ElasticSearch search result's documents
          elapsed: time used to search data in ElasticSearch
        
        """
        query = self.query_builder.create_elastic_query_search(query)
        search_result = self.client.search_data(query=query)
        documents = self.query_getter.get_documents_results(search_result)
        elapsed = self.query_getter.get_elastic_elapsed(search_result)
        return documents, elapsed

    def common_update(self, query: Dict, update: Dict, how: str = "one"):
        """
        ElasticSearch common update data operator.

        flow:
        json_data -> search_query -> database -> update_result
                     update_query             -> elapsed
                     how

        return:
          update_result: ElasticSearch update result
          elapsed: time used to update data in ElasticSearch
        
        """
        update_filter = self.query_builder.create_elastic_match_query(query)
        update_result = self.client.update_data(
            query=update_filter, update=update, how=how
        )
        elapsed = self.query_getter.get_elastic_elapsed(update_result)
        return update_result, elapsed

    def common_delete(self, query: Dict, how: str = "one"):
        """
        ElasticSearch common delete data operator.

        flow:
        json_data -> search_query -> database -> delete_result
                     how                      -> elapsed

        return:
          delete_result: ElasticSearch delete result
          elapsed: time used to delete data in ElasticSearch
        
        """
        delete_filter = self.query_builder.create_elastic_match_query(query)
        delete_result = self.client.delete_data(
            query=delete_filter, how=how
        )
        elapsed = self.query_getter.get_elastic_elapsed(delete_result)
        return delete_result, elapsed


mongo_operator = MongodbOperator(mongo_client)
elastic_operator = ElasticOperator(elastic_client)
