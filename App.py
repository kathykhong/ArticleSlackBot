import os
# Use the package we installed
from slack_bolt import App
from dotenv import load_dotenv
import json
import random

load_dotenv()

# Initializes your app with your bot token and signing secret
app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)

# Add functionality here
# @app.event("app_home_opened") etc

@app.command('/hellocapybara')
def sayHello(ack,respond,command, say):
    print("line 19")
    ack()
    say('hello Capybara')

@app.command('/speak')
def saySpeakingOrder(ack,command,say):
    commandDict = json.dumps(command)
    commandStr = json.loads(commandDict)
    names = []
    namesStr = ''
    
    if "text" in commandStr:
        commandText = commandStr["text"]
        names = commandText.split()
    else:
        channelID = commandStr["channel_id"]
        convoInfo = app.client.conversations_members(channel=channelID)
        members = convoInfo["members"]
        for member in members:
            userInfo = app.client.users_info(user=member)
            name = userInfo["user"]["real_name"]
            if name != 'SuperBot':
                names.append(name)

    random.shuffle(names)
    namesStr = '\n'.join(names)
    ack()
    say(namesStr)

# Start your app
if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))

