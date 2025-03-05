from typing import List

import asyncio

from elasticsearch import Elasticsearch
from pydantic_ai.messages import ModelMessage, ModelRequest, UserPromptPart, ModelResponse, TextPart

from es_agent import ElasticDeps, es_agent


class ESCLI:
    def __init__(self):
        self.messages: List[ModelMessage] = []
        self.deps = ElasticDeps(client=Elasticsearch([{'host': 'localhost', 'port': 9200, 'scheme': 'http'}]),
                                index_name='filebeat-8.17.1-2025')

    async def chat(self):
        print("GitHub Agent CLI (type 'quit' to exit)")
        print("Enter your message:")

        try:
            while True:
                user_input = input("> ").strip()
                if user_input.lower() == 'quit':
                    break

                # Run the agent with streaming
                result = await es_agent.run(
                    user_input,
                    deps=self.deps,
                    message_history=self.messages
                )

                # Store the user message
                self.messages.append(
                    ModelRequest(parts=[UserPromptPart(content=user_input)])
                )

                # Store itermediatry messages like tool calls and responses
                filtered_messages = [msg for msg in result.new_messages()
                                     if not (hasattr(msg, 'parts') and
                                             any(part.part_kind == 'user-prompt' or part.part_kind == 'text' for part in
                                                 msg.parts))]
                self.messages.extend(filtered_messages)

                # Optional if you want to print out tool calls and responses
                # print(filtered_messages + "\n\n")

                print(result.data)

                # Add the final response from the agent
                self.messages.append(
                    ModelResponse(parts=[TextPart(content=result.data)])
                )
        finally:
            await self.deps.client.close()


async def main():
    cli = ESCLI()
    await cli.chat()


if __name__ == "__main__":
    asyncio.run(main())