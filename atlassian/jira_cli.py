import os
from typing import List

import asyncio

from dotenv import load_dotenv
from jira import JIRA
from pydantic_ai.messages import ModelMessage, ModelRequest, UserPromptPart, ModelResponse, TextPart

from jira_agent import JiraDeps, jira_agent

load_dotenv()

class JiraCLI:
    def __init__(self):
        self.messages: List[ModelMessage] = []
        self.jira_url = os.getenv('JIRA_URL')
        self.api_token = os.getenv("JIRA_API_TOKEN")
        self.deps = JiraDeps(client=JIRA(server=self.jira_url,token_auth=self.api_token),project_key='AIPOC')

    async def chat(self):
        print("Jira Agent CLI (type 'quit' to exit)")
        print("Enter your message:")

        try:
            while True:
                user_input = input("> ").strip()
                if user_input.lower() == 'quit':
                    break

                # Run the agent with streaming
                result = await jira_agent.run(
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
            print("Closing Jira client")


async def main():
    cli = JiraCLI()
    await cli.chat()


if __name__ == "__main__":
    asyncio.run(main())