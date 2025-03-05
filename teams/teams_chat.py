import pymsteams

# Initialize the connector card with your webhook URL
myTeamsMessage = pymsteams.connectorcard("https://lufthansagroup.webhook.office.com/webhookb2/c479c698-e273-4c28-953f-e8301c2875ec@72e15514-5be9-46a8-8b0b-af9b1b77b3b8/IncomingWebhook/61483ac09fd14355a7e9f4f9989dc02c/430a462a-ff13-4b4e-ab74-73b3af3a0cdc/V2Yuk8Jw0jtG-7w3AYyu8N5-l7-auSWYrH76GJ_gD_ouc1")

# Set the message color
myTeamsMessage.color("#F8C471")

# Add your message text
myTeamsMessage.text("Check out this link: [Google](https://www.google.com)")

# Send the message
myTeamsMessage.send()
