from typing import List, Dict


# MongoDB Query Functions
# =======================
class MongodbQueryBuilder:
    """Class intended to create query for MongoDB"""

    def create_mongo_regex_search(self, filters: Dict):
        """
        Create mongoDB regex search from specified filters.

        It is a search using match format in:
        https://www.mongodb.com/docs/manual/reference/operator/query/regex/
        
        example:
        input <- {"name": "aji", "school": "eden"}
        output <- {"$regex": {"name": ".*aji.*", "school": ".*eden.*"}, "$options": "i" }

        """
        query_search = dict(filters)
        patterns = [f".*{value}.*" for value in filters.values()]
        regex_query = [{"$regex": pattern, "$options": "i"} for pattern in patterns]
        
        for field, query in zip(query_search.keys(), regex_query):
            query_search[field] = query
        return query_search

    def create_mongo_update_query(self, update):
        update_query = {"$set": update}
        return update_query


class MongodbQueryGetter:
    """Class intended to retrieve something from MongoDB query"""

    def get_mongo_elapsed(self, result):
        return result.explain()["executionStats"]["executionTimeMillis"]



# ElasticSearch Query Functions
# =============================
class EsQueryBuilder:
    """Class intended to create query for MongoDB"""
    
    def create_elastic_query_search(self, filters: Dict):
        """
        Create ElasticSearch query search from specified filters.
        
        It is a search using query string format in:
        https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-query-string-query.html
        
        example:
        input <- {"name": "aji", "school": "eden"}
        output <- {"query_string": {"fields": ["name", "school"], "query": "*aji* AND *eden*"}}
        
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

    def create_elastic_match_query(self, filters):
        match_query = {"match": filters}
        return match_query


class EsQueryGetter:
    """Class intended to retrieve something from ES query"""

    def get_documents_results(self, search_result):
        """
        Get documents from Elasticsearch results.
        
        The search results came with this format: 
        {..., hits: {..., hits: ..., _source:}}
        
        The data lies inside _source keys, therefore we need
        to access it.
        
        """
        documents = search_result["hits"]["hits"]
        if documents:
            documents = [doc["_source"] for doc in documents]
        return documents


    def get_elastic_elapsed(self, result):
        return result["took"]