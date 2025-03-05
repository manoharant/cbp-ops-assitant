from jira import JIRA

# Replace these with your Jira instance URL and credentials
jira_url = 'https://trackspace.lhsystems.com'
username = 'U776856'
api_token = 'ODc3NzY0MTA4ODcxOiBJ9mv0YoroEjadWSd6IVQllX9G'
# Connect to Jira
jira = JIRA(server=jira_url, token_auth=api_token)

#response = jira.search_issues('project="LCAGIM" AND labels = "EBOO" AND assignee in (lc.bookingengine.devops) ')
#response = jira.search_issues('project="LCAGIM" AND text ~"Embargo not shown in BookIT" AND (assignee was lc.bookingengine.devops OR assignee was lc.bookingengine.ops OR assignee in (lc.bookingengine.devops)) ORDER BY updatedDate DESC, createdDate ASC',maxResults=10)
#response = jira.search_issues('project="NEWBE" AND text ~"Embargo" AND issuetype in(Epic,Story) ORDER BY updatedDate DESC, createdDate ASC',maxResults=25)
response = jira.search_issues('project="NEWBE" AND key="LCAGIM-47895"',maxResults=25)


# Print the retrieved issues
for issue in response:
    print(f"Issue Key: {issue.key}, Summary: {issue.fields.summary}, assignee: {issue.fields.assignee}, status: {issue.fields.status}, updated: {issue.fields.updated}, created: {issue.fields.created}")