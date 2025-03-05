from jira import JIRA

# Replace these with your Jira instance URL and credentials
jira_url = 'https://manoharant.atlassian.net'
username = 'manoharant@gmail.com'
api_token = 'ATATT3xFfGF0z2tETfqzBNomWPdxMACIXRMlkMd4RjEKUtOdeypHun-ch4m28CgucDI5LJrdX3jpJg66nRpXx10lG8PCNYgQVM4kU63po59ZoRFsfVgazqZc0C3LR1bB_jnrepQOrKHt7LmIxpu6sov6fh15D8MVQLwOG4KAecJrwS1B6jHRN_g=88BE301E'

# Connect to Jira
jira = JIRA(server=jira_url, basic_auth=(username, api_token))

issue = jira.issue('AIPOC-75')
issue.update(fields={'labels': ['BOOKEMON']})
