import os

from dotenv import load_dotenv
from jira import JIRA

load_dotenv()
# Replace these with your Jira instance URL and credentials
jira_url = os.getenv('JIRA_URL')
api_token = os.getenv('JIRA_API_TOKEN')

# Connect to Jira
jira = JIRA(server=jira_url, token_auth=api_token)

issue = jira.issue('AIPOC-2')
# Create a new comment
jira.add_comment('AIPOC-2', 'hello, how are you doing?')
