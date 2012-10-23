#!/usr/bin/env python
import smtplib
from email.mime.text import MIMEText

pwd = '******'
me = 'marchenko.alexandr@gmail.com'
to = me

html = """\
<html>
  <head></head>
  <body>
    <p>Hi!<br>
       How are you?<br>
       Here is the <a href="http://www.python.org">link</a> you wanted.
    </p>
  </body>
</html>
"""

msg = MIMEText(html, 'html')

# me == the sender's email address
# you == the recipient's email address
msg['Subject'] = 'TEST'
msg['From'] = me
msg['To'] = to

server = smtplib.SMTP('smtp.gmail.com',587) #port 465 or 587
server.ehlo()
server.starttls()
server.ehlo()
server.login(me, pwd)
server.sendmail(me, to, msg)
server.close()
