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
print(f"host=localhost dbname={DB_NAME} user={DB_USER}")
def get_all():
    cur = conn.cursor()
    cur.execute('SELECT * FROM "TERMINAL_DATA" ORDER BY "id"')
    records = cur.fetchall()
    for record in records:
        print(record)
    return records

def get_last():
    cur = conn.cursor()
    cur.execute('SELECT * from "TERMINAL_DATA" ORDER BY "id" DESC LIMIT 1')
    record = cur.fetchall()
    print(record)
    return record

if __name__ == '__main__':
    get_all()
