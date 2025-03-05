import os
from dataclasses import dataclass

import logfire
from jira import JIRA
from openai import AsyncAzureOpenAI
from pydantic import BaseModel

from pydantic_ai import Agent, RunContext
from pydantic_ai.models.openai import OpenAIModel

logfire.configure()

system_prompt = """
    You are a atlassian jira expert with access to Jira to help the user manage the story,task and issue creation and get information from it.

    Your only job is to assist with this and you don't answer other questions besides describing what you are able to do.

    Don't ask the user before taking an action, just do it. Always make sure you look at the index with the provided tools before answering the user's question unless you have already.

    When answering a question about the query, always start your answer with the full details in brackets and then give your answer on a newline. Like:

    [Using [query from the user]]

    Your answer here...
    """



class JiraResponse(BaseModel):
    issue_key: str
    summary: str = None
    description: str = None
    comments: list[str] = None

@dataclass
class JiraDeps:
    client: JIRA
    project_key: str

#model = OpenAIModel(model_name='llama3.2:1b', base_url='http://localhost:11434/v1')
client = AsyncAzureOpenAI(
    azure_endpoint='https://cbp-ai-service.openai.azure.com/',
    api_version='2024-08-01-preview',
    api_key=os.getenv('AZURE_OPENAI_API_KEY'),
)
model = OpenAIModel('gpt-4o', openai_client=client)

jira_agent = Agent(
    model,
    system_prompt=system_prompt,
    deps_type=JiraDeps,
    retries=0
)

@jira_agent.tool
async def get_jira_issues(ctx: RunContext[JiraDeps],search_keyword:str) -> list[JiraResponse]:
    logfire.info(f"Searching for Jira issues with keyword: {search_keyword}")
    response = ctx.deps.client.search_issues(f"project={ctx.deps.project_key} AND text ~'{search_keyword}' AND (assignee was lc.bookingengine.devops OR assignee was lc.bookingengine.ops OR assignee in (lc.bookingengine.devops)) ORDER BY updatedDate DESC, createdDate ASC",maxResults=10)

    # Print the retrieved issues
    jira_issues = []
    for issue in response:
        jira_issues.append(JiraResponse(
            issue_key=issue.key,
            summary=issue.fields.summary,
            description=issue.fields.description,
            comments=[comment.body for comment in issue.fields.comment.comments]
        ))
    return jira_issues

@jira_agent.tool
async def get_jira_issue(ctx: RunContext[JiraDeps],key:str) -> list[JiraResponse]:
    logfire.info(f"Searching for Jira issue with key: {key}")
    response = ctx.deps.client.search_issues(f"project={ctx.deps.project_key} AND key={key}",maxResults=10)

    # Print the retrieved issues
    jira_issues = []
    for issue in response:
        jira_issues.append(JiraResponse(
            issue_key=issue.key,
            summary=issue.fields.summary,
            description=issue.fields.description,
            comments=[comment.body for comment in issue.fields.comment.comments]
        ))
    return jira_issues

@jira_agent.tool
async def create_jira_issue(ctx: RunContext[JiraDeps]) -> JiraResponse:
    """
    Create a new Jira issue.
    :param ctx: RunContext object containing the dependencies.
    :return: JiraResponse object containing the issue key and description.
    """
    # Define the search query
    issue_dict = {
        'project': {'key': ctx.deps.project_key},
        'summary': 'New issue from Jira-Python',
        'description': 'Creating an issue via automated script',
        'labels': ['BOOKEMON'],
        'issuetype': {'name': 'Bug'},
    }

    # Perform the search query on the specified index
    response = ctx.deps.client.create_issue(fields=issue_dict)

    # Extract the search results
    results = JiraResponse(
        issue_key=response.key,
        description=response.fields.description
    )

    return results

@jira_agent.tool
async def update_jira_issue(ctx: RunContext[JiraDeps],key:str,labels:list[str]) -> JiraResponse:
    """
    Update a Jira issue.
    :param ctx: RunContext object containing the dependencies.
    :param key: The key of the issue to be updated.
    :param labels: The list of labels to be added to the issue.This value should contain only "BOOKEMON" or "EBOO" and "QROOKS" or "UI".
    :return: JiraResponse object containing the updated issue key and description.
    """
    # Define the search query
    issue = ctx.deps.client.issue(key)
    issue.update(fields={'labels': labels})

    # Extract the search results
    results = JiraResponse(
        issue_key=issue.key,
        description=issue.fields.description
    )

    return results