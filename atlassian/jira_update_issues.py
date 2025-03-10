import os

from dotenv import load_dotenv
from jira import JIRA

load_dotenv()

# Replace these with your Jira instance URL and credentials
jira_url = os.getenv('JIRA_URL')
api_token = os.getenv('JIRA_API_TOKEN')

# Connect to Jira
jira = JIRA(server=jira_url, token_auth=api_token)

issue = jira.issue('AIPOC-75')
issue.update(fields={'labels': ['BOOKEMON']})
