import psycopg2
import os
# import smtplib
from dotenv import load_dotenv
# from email.message import EmailMessage
load_dotenv()

DB_USER = os.getenv('DB_USER')
DB_PW = os.getenv('DB_PW')
DB_NAME = os.getenv('DB_NAME')

conn = psycopg2.connect(f"host=localhost dbname={DB_NAME} user={DB_USER} password={DB_PW}")
def get_all():
    cur = conn.cursor()
    cur.execute('SELECT * FROM "TERMINAL_DATA"')
    records = cur.fetchall()
    # print(records)
    return records

def get_last():
    cur = conn.cursor()
    cur.execute('SELECT * from "TERMINAL_DATA" ORDER BY "lastTransaction" DESC LIMIT 1')
    record = cur.fetchall()
    print(record)
    return record

