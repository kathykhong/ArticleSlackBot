import os
import json
import requests
# Use the package we installed
from slack_bolt import App, response
from dotenv import load_dotenv
# headers = {"Authorization": "Bearer tmrp5rrXRcf4xMegTWmRCVjvyusMZ1YUBBuv33iMSIQsGuRmOpAtL831JkwKOdlEes8WFuT9j2DRm_K63-xemzCfeGoc85BCBNA3bXny0Gz7N2ov5mJwfHFb"}

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

request = requests.post('https://bitbucket.org/site/oauth2/authorize')

@app.command('/prs')
def showPRs(ack,command,say):
    ack()

    commandDict = json.dumps(command)
    commandStr = json.loads(commandDict)
    print(commandStr)
    

    if "text" in commandStr:
        repoName = commandStr["text"]
        print(repoName)
        url="https://bitbucket.org/!api/2.0/repositories/articledev/{}/pullrequests".format(repoName)
        print(url)

        response = requests.get(url, headers = {"Authorization": "Bearer 30_UNFGGudTn56nGqt4enyLqCMu0AD90_AF7FKPbFMdXaUIOmLFl8Nf7nMyt43W5P_O6ZLny6JPXdYEYFIx6q0oTqi2vhhcau2F9Qyh8tCNUM5Sf0whqZX3d"})
        # data = response.json()
        # print(data) 
        # print("the status is" + str(response.status_code))
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
    




# Start your app
if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))

