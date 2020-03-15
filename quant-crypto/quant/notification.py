import smtplib
import json
from email.message import EmailMessage
import winsound

with open('./quant/config.json') as json_file:
    data = json.load(json_file)
    GMAIL_USER = data['gmail']['user']
    GMAIL_PASSWORD = data['gmail']['password']
    SUBSCRIBERS = data['subscribers']

def notification(source, ticker, interval, timeframe, url):
    print("not start")
    winsound.Beep(700, 1000)
    msg = EmailMessage()
    msg['From'] = GMAIL_USER

    msg['To'] = SUBSCRIBERS
    msg['Subject'] = f'{source} {ticker}'

    msg.set_content("\n" + source + " has been detected on " + ticker + " on timeframe : " + str(interval) + \
                    timeframe.name + "\n" + url)
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(GMAIL_USER, GMAIL_PASSWORD)
        server.send_message(msg)
        server.close()
        print('Email sent!')
    except Exception as e:
        print(e)
        print('Something went wrong...')
