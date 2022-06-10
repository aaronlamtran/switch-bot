import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

SLACK_TOKEN=os.getenv('SLACK_TOKEN')

client = WebClient(token=SLACK_TOKEN)

client.chat_postMessage(channel='#switch-monitoring', text='hello world')


