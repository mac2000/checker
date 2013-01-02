#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import smtplib
from email.mime.text import MIMEText

def notify(gmail_from, to, subject, body, gmail_smtp_password):
    msg = MIMEText(body, 'html')
    msg['Subject'] = subject
    msg['From'] = gmail_from
    msg['To'] = to

    smtp = smtplib.SMTP('smtp.gmail.com',587)
    smtp.ehlo()
    smtp.starttls()
    smtp.ehlo()
    smtp.login(gmail_from, gmail_smtp_password)
    smtp.sendmail(gmail_from, to, msg.as_string())
    smtp.close()

