import os
import requests
import json
import random
from slack_bolt import App
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)

@app.command('/hellocapybara')
def sayHello(ack,say):
    ack()
    say('hello Capybara')

@app.command('/scrum')
def GenerateScrumOrderAndWordOfTheDay(ack,command,say):
    ack()
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
            if name != 'Capybara':
                names.append(name)

    random.shuffle(names)
    namesStr = '\n'.join(names)
    say(scrapeWordOfTheDay() + '\n\n\n' + namesStr)

def scrapeWordOfTheDay():
    url = 'https://www.dictionary.com/e/word-of-the-day/'
    try:
        r = requests.get(url)
        r.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)

    soup = BeautifulSoup(r.content, 'html.parser')

    date = soup.find('div', class_='otd-item-headword__date').text.strip()
    word = soup.find('div', class_='otd-item-headword__word').text.strip()
    pronunciation = soup.find('div', class_='otd-item-headword__pronunciation').text.strip()
    definition = soup.find('div', class_='otd-item-headword__pos-blocks').text.strip()

    wordOfTheDay = '*' + date + '*' + '\n' + word + '\n' + pronunciation + '\n' + definition

    return wordOfTheDay

if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))

