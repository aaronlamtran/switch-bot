from curses import curs_set
from pydoc import doc
from pymongo import MongoClient
import pymongo
from dotenv import load_dotenv
import os
from operator import attrgetter, itemgetter
import smtplib
from email.message import EmailMessage

load_dotenv()

SEND_TO_EMAIL_ADDRESS = os.getenv('SEND_TO_EMAIL_ADDRESS')
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
    for document in cursor:
        _id, name, email, phone, dog, waitlistPosition, createdAt, updatedAt = itemgetter('_id', 'name', 'email', 'phone', 'dog', 'waitlistPosition', 'createdAt', 'updatedAt')(document)
        # print(name, email, phone, createdAt)
        waitlist_str += name + space + email + space + phone + space  + str(createdAt) + '\n'

        # mylist.append(document)
    # tilde = "~" * 30
    print(waitlist_str)
    print("~" * 30)

    for collection in all_collections:
      print(collection)
    return waitlist_str

def email_one(payload):
    msg = EmailMessage()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = SEND_TO_EMAIL_ADDRESS
    message = payload
    msg['Subject'] = f'someone joined!'
    msg.set_content(message)
    print(msg)
    server = smtplib.SMTP_SSL('smtp.mail.yahoo.com', 465)
    server.ehlo()
    server.login(EMAIL_ADDRESS, EMAIL_PW)
    server.send_message(msg)
    print('email sent')

if __name__ == "__main__":
    get_waitlist()

# {'_id': ObjectId('62eaffade9c26e12d5145f64'), 'name': 'Jen Foster', 'email': 'soccerjen2000@hotmail.com', 'phone': '+1 (760) 855-8311', 'dog': ObjectId('6258e5b0e351100c23230d02'), 'waitlistPosition': 40, 'createdAt': datetime.datetime(2022, 8, 3, 23, 7, 25, 133000), 'updatedAt': datetime.datetime(2022, 8, 3, 23, 7, 25, 133000), '__v': 0}
