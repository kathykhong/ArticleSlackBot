import os
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
    print("line 29")
    ack()
    response = requests.get("https://bitbucket.org/!api/2.0/repositories/articledev/kraken-product/pullrequests", headers = {"Authorization": "Bearer eieVj2-lQNlEct-6-qb4llPSsG2NZ6tnK_h5ppmBBnJOmRMr6_fYqcTtF1sJS46WFQsFw5xJQLnb-yxwmdl9oX2yblMWGSAz6542smqv028VdEa56ZZFvKlV"})
    if response.status_code == 200:
        print('Success!')
    elif response.status_code == 404:
        print('Not Found.')
    data = response.json()
    print(data)
    say("prs")

# Start your app
if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))

