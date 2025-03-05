from elasticsearch import Elasticsearch

# Connect to the Elasticsearch instance
es = Elasticsearch([{'host': 'localhost', 'port': 9200, 'scheme': 'http'}])

# Define the search query
search_query = {
    "query": {
        "match": {
            "conversationid": '55da3c53-0987-41b0-8ac5-b572b2d233ff'
        }
    },
    "size": 1000,
    "_source": ["conversationid","message","timestamp","payload"]
}

# Perform the search query on the specified index
index_name = 'filebeat-8.17.1-2025.02.05'
response = es.search(index=index_name, body=search_query)

# Print the search results
for hit in response['hits']['hits']:
    print(hit['_source'])