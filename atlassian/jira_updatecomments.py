import os

from jira import JIRA

# Replace these with your Jira instance URL and credentials
jira_url = os.getenv('JIRA_URL')
username = os.getenv('JIRA_USERNAME')
api_token = os.getenv('JIRA_API_TOKEN')

# Connect to Jira
jira = JIRA(server=jira_url, basic_auth=(username, api_token))

issue = jira.issue('AIPOC-75')
# Create a new comment
jira.add_comment('AIPOC-75', 'hello, how are you doing?')
