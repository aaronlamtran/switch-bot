import os
from slack_sdk import WebClient

# from slack-client import WebClient
from slack_sdk.errors import SlackApiError
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask
from flask import send_file
from flask import Response
from flask import request
from controllers import get_all, get_last
from frenchie_controllers import get_waitlist, email_one
from fan import Fan
import json

load_dotenv()

SLACK_TOKEN = os.getenv("SLACK_TOKEN")

client = WebClient(token=SLACK_TOKEN)

app = Flask(__name__)
bedroom_fan = Fan()


@app.route("/")
def hello_world():
    return "<p>Switch Bot</p>"

@app.route("/nfl")
def feed_scoreboard():
    return send_file('live_scores.txt')


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

@app.route("/frenchie", methods=["GET"])
def email_frenchie():
    email_payload =  get_waitlist()
    email_one(email_payload)
    return 'sent'

# iot
@app.route("/status")
def get_status():
    return bedroom_fan.get_status_fan()

@app.route("/status", methods=['POST'])
def set_status():
    req = request.json
    return bedroom_fan.set_status(req)



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
