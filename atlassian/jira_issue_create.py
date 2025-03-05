from jira import JIRA

# Replace these with your Jira instance URL and credentials
jira_url = 'https://manoharant.atlassian.net'
username = 'manoharant@gmail.com'
api_token = 'ATATT3xFfGF0rAfbxoDY9QMUKuvXZLEwzSxGC3rbwTH1nsuCXDlL7tSKQ5FT2Kq59yg4Q2AWzcTFtrHHEihY0yxX7fM9IFaDbDW0_n7VqMda59kXNVE5-aiAw27C1NY3h0W6fMA-e8JenDXh85rO4CA7BoOkzKDriGPHop9feUeeoAGXmJ3Z6_A=2E0BB3E5'

issue_url = f"test/app/discover#/?_g=(filters:!(),refreshInterval:(pause:!t,value:60000),time:(from:now-15d,to:now))&_a=(columns:!(),dataSource:(dataViewId:e7f67bce-8dab-44a2-901c-2eb65e595ea5,type:dataView),filters:!(),interval:auto,query:(language:kuery,query:%22test%22),sort:!(!('@timestamp',desc)))"

# Connect to Jira
jira = JIRA(server=jira_url, basic_auth=(username, api_token))
issue_description = f"""
https://manoharant.atlassian.net/browse/AIPOC-75%29%29%29
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