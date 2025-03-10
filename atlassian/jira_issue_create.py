import os

from dotenv import load_dotenv
from jira import JIRA

load_dotenv()

# Replace these with your Jira instance URL and credentials
jira_url = os.getenv('JIRA_URL')
api_token = os.getenv("JIRA_API_TOKEN")

issue_url = f"test/app/discover#/?_g=(filters:!(),refreshInterval:(pause:!t,value:60000),time:(from:now-15d,to:now))&_a=(columns:!(),dataSource:(dataViewId:e7f67bce-8dab-44a2-901c-2eb65e595ea5,type:dataView),filters:!(),interval:auto,query:(language:kuery,query:%22test%22),sort:!(!('@timestamp',desc)))"

# Connect to Jira
jira = JIRA(server=jira_url, token_auth=api_token)
issue_description = f"""
{os.getenv('JIRA_URL')}/browse/AIPOC-75%29%29%29
"""
# Define the issue details
issue_dict = {
    'project': {'key': 'AIPOC'},
    'summary': 'New issue from Jira-Python',
    'description': issue_description,
    'issuetype': {'name': 'Task'},
}

# Create the issue
new_issue = jira.create_issue(fields=issue_dict)

print(f"Issue {new_issue.key} created successfully.")