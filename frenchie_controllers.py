from curses import curs_set
from pydoc import doc
from re import S
from pymongo import MongoClient
import pymongo
from dotenv import load_dotenv
import os
from operator import attrgetter, itemgetter
import smtplib
from email.message import EmailMessage

load_dotenv()

SEND_TO_EMAIL_ADDRESS = os.getenv('SEND_TO_EMAIL_ADDRESS')
SEND_TO_EMAIL_ADDRESS_B = os.getenv('SEND_TO_EMAIL_ADDRESS_B')
TEST_TO_EMAIL_ADDRESS = os.getenv('TEST_TO_EMAIL_ADDRESS')
TEST_TO_EMAIL_ADDRESS_B = os.getenv('TEST_TO_EMAIL_ADDRESS_B')
PY_ENV = os.getenv('PY_ENV')


if PY_ENV == 'development':
    DEST_EMAIL = TEST_TO_EMAIL_ADDRESS
    DEST_EMAIL_B = TEST_TO_EMAIL_ADDRESS_B
if PY_ENV == 'production':
    DEST_EMAIL = SEND_TO_EMAIL_ADDRESS
    DEST_EMAIL_B = SEND_TO_EMAIL_ADDRESS_B


EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
EMAIL_PW = os.getenv('EMAIL_PW')
CONNECTION_STRING = os.getenv('FRENCHIE_DB_URI')


def get_waitlist():

    cluster = MongoClient(CONNECTION_STRING)
    waitlists = cluster[cluster.list_database_names()[0]].get_collection('waitlists')
    cursor = waitlists.find({})
    waitlist_str = ''
    space = " "
    line_break = space + "\n"
    count = 1
    for document in cursor:
        _id, name, email, phone, dog, waitlistPosition, createdAt, updatedAt = itemgetter(
            '_id', 'name', 'email', 'phone', 'dog', 'waitlistPosition', 'createdAt', 'updatedAt')(document)

        if not phone:
            phone = '#_NOT_PROVIDED'
        waitlist_str += str(count) + ". " + name + line_break + email + \
            line_break + phone + line_break + str(createdAt) + '\n\n'
        count += 1

        # mylist.append(document)
    # tilde = "~" * 30
    print(waitlist_str)
    print(DEST_EMAIL, DEST_EMAIL_B)

    return waitlist_str

def email_one(payload):
    recipients = [DEST_EMAIL, DEST_EMAIL_B]
    recipients = ", ".join(recipients)
    subject = 'Someone joined the TFC waitlist!'

    msg = EmailMessage()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = recipients
    msg['Subject'] = subject
    msg.set_content(payload)
    print(msg)

    server = smtplib.SMTP_SSL('smtp.mail.yahoo.com', 465)
    server.ehlo()
    server.login(EMAIL_ADDRESS, EMAIL_PW)
    server.send_message(msg)
    print('email sent')


if __name__ == "__main__":
    get_waitlist()


