import os

import chainlit as cl
from openai import AsyncAzureOpenAI
from pydantic import BaseModel
from pydantic_ai import Agent, BinaryContent
from pydantic_ai.models.openai import OpenAIModel

class ImageSummary(BaseModel):
    description: str
    objects_detected: list[str]
    actions_identified: list[str]


@cl.on_message
async def on_message(msg: cl.Message):
    if not msg.elements:
        await cl.Message(content="No file attached").send()
        return

    # Processing images exclusively
    images = [file for file in msg.elements if "image" in file.mime]

    print(images)

    # Read the first image
    with open(images[0].path, "r") as f:
        pass

    # model = OpenAIModel(model_name='llama3.2:1b', base_url='http://localhost:11434/v1')
    client = AsyncAzureOpenAI(
        azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT'),
        api_version=os.getenv('AZURE_OPENAI_API_VERSION'),
        api_key=os.getenv('AZURE_OPENAI_API_KEY'),
    )
    model = OpenAIModel(os.getenv('AZURE_OPENAI_MODEL_NAME'), openai_client=client)
    agent = Agent(model=model)

    print(f"Images: {images[0].path}")
    # Read the local image
    with open(images[0].path, 'rb') as file:
        image_data = file.read()

    # Analyze the image using OpenAI's LLM
    response = agent.run_sync(
        [
            'What company is this logo from?',
            BinaryContent(data=image_data, media_type='image/jpeg'),
        ]
    )
    print(response.data)
    await cl.Message(content=response.data).send()
