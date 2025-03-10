import os

from jira import JIRA

# Replace these with your Jira instance URL and credentials
jira_url = 'https://manoharant.atlassian.net'
username = 'manoharant@gmail.com'
api_token = os.getenv('JIRA_API_TOKEN')

# Connect to Jira
jira = JIRA(server=jira_url, basic_auth=(username, api_token))

issue = jira.issue('AIPOC-75')
# Create a new comment
jira.add_comment('AIPOC-75', 'hello, how are you doing?')
