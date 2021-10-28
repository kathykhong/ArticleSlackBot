import os
import requests
from dotenv import load_dotenv
from slack_bolt import App
from bs4 import BeautifulSoup

load_dotenv()

# Initializes your app with your bot token and signing secret
app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)

@app.command('/hellocapybara')
def sayHello(ack,command,say):
    ack()
    say('hello Capybara')

@app.command('/wotd')
def scrapeWotd(ack,command,say):
    ack()

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

    say(wordOfTheDay)

# Start your app
if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))

