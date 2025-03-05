from elasticsearch import Elasticsearch
from elasticsearch_dsl import Q, Search
from pydantic.dataclasses import dataclass

# Initialize Elasticsearch client
es = Elasticsearch([{'host': 'localhost', 'port': 9200, 'scheme': 'http'}])
def build_dynamic_or_query(field_name, values):
    should_clauses = [Q('match', **{field_name: value}) for value in values]
    query = Q('bool', should=should_clauses, minimum_should_match=1)
    return query

# Example JSON input
@dataclass
class Result:
    conversationid: str
    message: str
    payload: str

# Build and execute the query
s = Search(using=es, index='filebeat-8.17.1-2025')
dynamic_query = build_dynamic_or_query("message", ["Response", "Payload"])
print(dynamic_query)
s = s.query(dynamic_query)

# Execute the search
response = s.execute()

# Print results
# Convert the search results to Result objects
results = []
for hit in response['hits']['hits']:
    source = hit['_source']
    result = Result(
        conversationid=source.conversationid,
        message=source.message,
        payload=source.payload
    )
    results.append(result)
print(results)
