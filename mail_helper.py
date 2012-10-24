#!/usr/sbin/env python
# -*- coding: utf-8 -*-
import smtplib
from email.mime.text import MIMEText

def send(to, subject, body):
    mail_from = 'marchenko.alexandr@gmail.com'
    smtp_pass = '5340940'

    msg = MIMEText(body, 'html')
    msg['Subject'] = subject
    msg['From'] = mail_from
    msg['To'] = to

    smtp = smtplib.SMTP('smtp.gmail.com',587)
    smtp.ehlo()
    smtp.starttls()
    smtp.ehlo()
    smtp.login(mail_from, smtp_pass)
    smtp.sendmail(mail_from, to, msg.as_string())
    smtp.close()
