from jira import JIRA

# Replace these with your Jira instance URL and credentials
jira_url = 'https://manoharant.atlassian.net'
username = 'manoharant@gmail.com'
api_token = 'ATATT3xFfGF0xzpeDDXWq7roWglhJcHZ6XIB3THZSUxgfxZomH8iLBaYzmDIuGA_92kOxlVVlKIjtQjdc_RNR6zNxid9HAoy8UPxqWWguH3KJa6vHbPIrSmIABtQY57oKJlaWnF-DDlzMyrnOiElk8RL3U4zKAi5iwBXuPpJPA49ZObPbx7ooBY=C6607C1F'

# Connect to Jira
jira = JIRA(server=jira_url, basic_auth=(username, api_token))

issue = jira.issue('AIPOC-75')
# Create a new comment
jira.add_comment('AIPOC-75', 'hello, how are you doing?')
