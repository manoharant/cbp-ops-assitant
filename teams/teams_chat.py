import os

import pymsteams

# Initialize the connector card with your webhook URL
myTeamsMessage = pymsteams.connectorcard(os.getenv('MS_TEAMS_WEBHOOK_URL'))

# Set the message color
myTeamsMessage.color("#F8C471")

# Add your message text
myTeamsMessage.text("Check out this link: [Google](https://www.google.com)")

# Send the message
myTeamsMessage.send()
