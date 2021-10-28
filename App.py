import os
import json
import requests
import random
from slack_bolt import App
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)

@app.command('/hellocapy')
def sayHello(ack,say):
    ack()
    greeting = "Hi! I'm Capy the Butler. I'm here to give you the word of the day, daily stand up support, and list pull requests for your repo."
    say(greeting)



@app.command('/prs')
def showPRs(ack,command,say):
    ack()

    commandDict = json.dumps(command)
    commandStr = json.loads(commandDict)
   
    

    if "text" in commandStr:
        repoName = commandStr["text"]

        url="https://bitbucket.org/!api/2.0/repositories/articledev/{}/pullrequests".format(repoName)
       

        response = requests.get(url, headers = {"Authorization": "Bearer <<oAuth access token>>"})
        
       
        if response.status_code == 200:
            print('Success!')
            data = response.json()
            
            
            if "values" in data:
                pullrequestslist = data["values"]
                megaString = '*' + "PRS to review for the " + repoName + " repo" + ":" +  '*' '\n'
                for pr in pullrequestslist:
                    title = pr["title"]
                    authorObject = pr["author"]
                    author = authorObject["display_name"]
                    linkObject = pr["links"]
                    htmlObject = linkObject["html"]
                    link=htmlObject["href"]
                    megaString = megaString + '*' + title + '*' + '\n' + "Author: " + author + '\n' + link + '\n' + '\n'
        
            say(megaString)
        elif response.status_code == 404:
            print('Not Found.')
           
    else: 
        say("Command is missing the name of the repository. Please try again:)")
    



@app.command('/scrum')
def generateScrumOrderAndWordOfTheDay(ack,command,say):
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

