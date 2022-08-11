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
EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
EMAIL_PW = os.getenv('EMAIL_PW')
CONNECTION_STRING = os.getenv('FRENCHIE_DB_URI')


def get_waitlist():
    mylist = []
    cluster = MongoClient(CONNECTION_STRING)
    main_db = cluster.list_database_names()[0]
    frenchie_collection = cluster[main_db]
    all_collections = frenchie_collection.list_collection_names()
    waitlists = frenchie_collection.get_collection('waitlists')
    cursor = waitlists.find({})
    waitlist_str = ''
    space = " "
    line_break = space + "\n"
    count = 1
    for document in cursor:
        _id, name, email, phone, dog, waitlistPosition, createdAt, updatedAt = itemgetter(
            '_id', 'name', 'email', 'phone', 'dog', 'waitlistPosition', 'createdAt', 'updatedAt')(document)
        # print(name, email, phone, createdAt)
        if not phone:
            phone = '#_NOT_PROVIDED'
        waitlist_str += str(count) + ". " + name + line_break + email + \
            line_break + phone + line_break + str(createdAt) + '\n\n'
        count += 1

        # mylist.append(document)
    # tilde = "~" * 30
    print(waitlist_str)
    print("~" * 30)

    for collection in all_collections:
        print(collection)
    return waitlist_str


def email_one(payload):
    recipients = []
    recipients.append(SEND_TO_EMAIL_ADDRESS)
    recipients.append(SEND_TO_EMAIL_ADDRESS_B)
    msg = EmailMessage()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = ", ".join(recipients)
    message = payload
    msg['Subject'] = 'Someone joined the TFC waitlist!'
    msg.set_content(message)
    print(msg)
    server = smtplib.SMTP_SSL('smtp.mail.yahoo.com', 465)
    server.ehlo()
    server.login(EMAIL_ADDRESS, EMAIL_PW)
    server.send_message(msg)
    print('email sent')


if __name__ == "__main__":
    get_waitlist()


