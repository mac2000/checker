#!/usr/bin/env python
import smtplib
from email.mime.text import MIMEText

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
msg['From'] = 'from@example.com'
msg['To'] = 'to@example.com'

# Send the message via our own SMTP server, but don't include the
# envelope header.
s = smtplib.SMTP('localhost')
s.sendmail('from@example.com', 'to@example.com', msg.as_string())
s.quit()

'''
from email.mime.text import MIMEText
from subprocess import Popen, PIPE

msg = MIMEText("Here is the body of my message")
msg["From"] = "me@example.com"
msg["To"] = "you@example.com"
msg["Subject"] = "This is the subject."
p = Popen(["/usr/sbin/sendmail", "-t"], stdin=PIPE)
p.communicate(msg.as_string())
'''
