import os
from slack_sdk import WebClient

# from slack-client import WebClient
from slack_sdk.errors import SlackApiError
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask
from flask import Response
from flask import request
from controllers import get_all, get_last
import json

load_dotenv()

SLACK_TOKEN = os.getenv("SLACK_TOKEN")

client = WebClient(token=SLACK_TOKEN)

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World! ... From Switch Bot</p>"


@app.route("/slashcommands", methods=["GET", "POST"])
def get_transactions():
    data = request.form
    print(data)
    index, date, term_id, balance, dtr, last_trans = get_last()
    return f"""
    {index}
    term_id: {term_id}
    balance: {balance}
    dtr: {dtr} days
    last txn: {last_trans}
    """


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
