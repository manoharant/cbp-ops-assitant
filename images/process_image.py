import os
import logging

from openai import AsyncAzureOpenAI
from pydantic_ai import Agent, BinaryContent
from pydantic_ai.models.openai import OpenAIModel

# Set up logging
logging.basicConfig(level=logging.DEBUG)

client = AsyncAzureOpenAI(
    azure_endpoint='https://cbp-hackathon-ai.openai.azure.com/',
    api_version='2024-08-01-preview',
    api_key='16kztm03Sxkv6lWpzPJnlrzWRsIaJq0ShIkFSTnMxMQzmDZ9BDkvJQQJ99BBACfhMk5XJ3w3AAABACOGhGf5',
)
model = OpenAIModel('gpt-4o-mini', openai_client=client)
# Initialize the agent with an OpenAI model
agent = Agent(model=model)

# Read the local image
with open('fantom-architecture.jpg', 'rb') as file:
    image_data = file.read()

# Log the binary data length to ensure it is read correctly
logging.debug(f"Image data length: {len(image_data)} bytes")

# Analyze the image using OpenAI's LLM
response =  agent.run_sync(
    [
        'What company is this logo from?',
        BinaryContent(data=image_data, media_type='image/jpeg'),
    ]
)

# Print the response
print(response.data)
