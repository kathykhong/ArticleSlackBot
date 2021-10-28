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
    convertToDict = json.dumps(command)
    convertDictToString = json.loads(convertToDict)
    if "text" in convertDictToString:
        inputString = convertDictToString["text"]
        names = inputString.split()
        random.shuffle(names)
        outputString = ' '.join(names)
        ack()
        say(outputString)
    else:
        channelID = convertDictToString["channel_id"]
        convoInfo = app.client.conversations_members(channel=channelID)
        members = convoInfo["members"]
        names = []
        for member in members:
            moreGarbage = app.client.users_info(user=member)
            name = moreGarbage["user"]["real_name"]
            if name != 'SuperBot':
                names.append(name)
        random.shuffle(names)
        outputString = ' '.join(names)
        ack()
        say(outputString)

# Start your app
if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))

