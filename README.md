# ArticleSlackBot

## Initial Setup

1. Install Python:
  - Mac: https://www.python.org/downloads/macos/ 
  - Windows: https://www.python.org/downloads/windows/
2. In Applications -> Python, open the `Install Certificates.command` file
3. Install ngrok: https://ngrok.com/download
4. Move the ngrok file into /usr/local/bin: `mv ngrok /usr/local/bin`
5. In ArticleSlackBot terminal, install the dependencies using the following (`pip` or `pip3`):
```
pip install -r requirements.txt
```


## Running the App (Locally)

In local terminal: `ngrok http 3000`

In ArticleSlackBot terminal:
```
python3 -m venv .venv
source .venv/bin/activate
python3 app.py
```

## Local development

### Adding new dependencies:
Whenever you add a new dependencies (`pip install` or otherwise) we need to add it to our requirements. This way anyone can just execute `pip install -r requirements.txt` and they should have everything they need to run and develop this app. 
```
pip freeze
pip install -r requirements.txt
```
### Creating a new slash command:

1. Run ngrok locally: `ngrok http 3000`
2. On the Slack App Dashboard -> Features -> Slash Commands:
     - Create New Command
     - Fill in the required fields: Command, Request URL and Short Description
     - Set the Request URL to the ngrok url, followed by `/slack/events` (eg. https://e5e9-216-19.ngrok.io/slack/events)
     - Click Save
3. In App.py:
```
@app.command('/commandname')
def sayHelloCapybara(ack,say):
    ack()
    say('Hello Capybara')
```
4. Run the app: `python3 app.py`
5. Test the command in Slack


## Troubleshooting

### Import errors such as "no module named slack_bolt":
- Run `python -m pip install slack_bolt` or `python3 -m pip install slack_bolt`
- If error still occurs:
    - `pip uninstall slack_bolt`
    - restart IDE
    - `pip install slack_bolt`

### Internal Server Error 500 on ngrok:
- In `pyenv.cfg`, ensure that `home = /usr/local/bin`

### Slack error "displatch_failed"
- Ensure your ngrok server and slack backend are up and running properly
