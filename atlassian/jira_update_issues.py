import os

from jira import JIRA

# Replace these with your Jira instance URL and credentials
jira_url = 'https://manoharant.atlassian.net'
username = 'manoharant@gmail.com'
api_token = os.getenv('JIRA_API_TOKEN')

# Connect to Jira
jira = JIRA(server=jira_url, basic_auth=(username, api_token))

issue = jira.issue('AIPOC-75')
issue.update(fields={'labels': ['BOOKEMON']})
