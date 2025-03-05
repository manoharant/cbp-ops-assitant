import os
from dataclasses import dataclass
from typing import Any, Coroutine

from elastic_transport import ObjectApiResponse
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Q, Search
from openai import AsyncAzureOpenAI

from pydantic_ai import Agent, ModelRetry, RunContext
from pydantic_ai.models.openai import OpenAIModel

system_prompt = """
    You are a elastic expert with access to Elasticsearch to help the user manage the log index and get information from it.

    Your only job is to assist with this and you don't answer other questions besides describing what you are able to do.

    Don't ask the user before taking an action, just do it. Always make sure you look at the index with the provided tools before answering the user's question unless you have already.

    When answering a question about the query, always start your answer with the full details in brackets and then give your answer on a newline. Like:

    [Using [query from the user]]

    Your answer here...
    """

@dataclass
class ESResponse:
    results: list[dict]

@dataclass
class Result:
    conversationid: str
    message: str
    payload: str

@dataclass
class ElasticDeps:
    client: Elasticsearch
    index_name: str
    supporting_keys: list[str]

#model = OpenAIModel(model_name='llama3.2:1b', base_url='http://localhost:11434/v1')
client = AsyncAzureOpenAI(
    azure_endpoint='https://cbp-ai-service.openai.azure.com/',
    api_version='2024-08-01-preview',
    api_key=os.getenv('AZURE_OPENAI_API_KEY'),
)
model = OpenAIModel('gpt-4o', openai_client=client)

es_agent = Agent(
    model,
    system_prompt=system_prompt,
    deps_type=ElasticDeps,
    retries=0
)


@es_agent.tool
async def get_result_conversation_id(ctx: RunContext[ElasticDeps], conversationid: str) -> ObjectApiResponse[Any]:
    """
    Get the result of an Elasticsearch query by conversation ID.This method only will be called if the conversation ID is provided.

    :param ctx: agent context
    :param conversationid: conversation ID to extract the result
    :return: ESResponse containing the search results
    """
    # Define the search query
    search_query = {
        "query": {
            "match": {
                "conversationid": conversationid
            }
        },
        "size": 10,
        "_source": ["conversationid", "message", "payload"]
    }

    # Perform the search query on the specified index
    response = ctx.deps.client.search(index=ctx.deps.index_name, body=search_query)


    # Convert the search results to Result objects
    results = []
    for hit in response['hits']['hits']:
        source = hit['_source']
        result = Result(
            conversationid=source.get('conversationid', ''),
            message=source.get('message', ''),
            payload=source.get('payload', '')
        )
        results.append(result)

    return results



@es_agent.tool
async def search_for_query_string(ctx: RunContext[ElasticDeps], search_keyword: str) -> ObjectApiResponse[Any]:
    """
    This method is used to search for a query string in the Elasticsearch index.Please form the query string in a way that it can be used to search in the index.
    To form a query string, you can use the booking_keys.csv and routeoffer_keys.csv files and these files contain the keys that are used in the query string.
    :param ctx: agent context
    :param search_keyword: search keyword to extract the result from the index. search keyword should be in the form of a query string and this can be formed using the keys in context.
    :return: ESResponse containing the search results
    """
    try:
        print(f"Delegating to Elasticsearch agent with search_string: {search_keyword}")

        # Split the search keyword into individual words
        #keywords = search_keyword.split()
        search_query = build_dynamic_or_query("message", [search_keyword])

        print(f"Constructed search query: {search_query}")

        # Define the search query using elasticsearch_dsl
        s = Search(using=ctx.deps.client, index=ctx.deps.index_name)
        s = s.query(search_query)

        # Execute the search
        response = s.execute()

        # Log the raw response for debugging
        print(f"Raw response from Elasticsearch: {response.to_dict()}")

        # Convert the search results to Result objects
        results = []
        for hit in response['hits']['hits']:
            source = hit['_source']
            result = Result(
                conversationid=source.conversationid if hasattr(source, 'conversationid') else '',
                message=source.message if hasattr(source, 'message') else '',
                payload=source.payload if hasattr(source, 'payload') else ''
            )
            results.append(result)

        return results

    except KeyError as e:
        print(f"KeyError: {e} - Check if the expected keys are present in the response")
        raise
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise




# Define a function to dynamically build the query
def build_dynamic_or_query(field_name, values):
    should_clauses = [Q('match', **{field_name: value}) for value in values]
    query = Q('bool', should=should_clauses, minimum_should_match=1)
    return query

