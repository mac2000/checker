#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import pika
import sys
import MySQLdb
import ConfigParser
import json
import smtplib
from email.mime.text import MIMEText

# Read config.ini
config = ConfigParser.ConfigParser()
config.read(os.path.expanduser('~/www/checker/config.ini'))

queue_name = 'proxy_check'

# Connect to RabbitMQ
rabbit = pika.BlockingConnection(pika.ConnectionParameters(
	host=config.get('rabbitmq', 'host'),
	port=int(config.get('rabbitmq', 'port')),
	credentials=pika.PlainCredentials(
		config.get('rabbitmq', 'user'),
		config.get('rabbitmq', 'pass')
	)
))
channel = rabbit.channel()
queue = channel.queue_declare(queue=queue_name, durable=True)
message_count = queue.method.message_count

# Connect to MySQL
dbh = MySQLdb.connect(
	config.get('mysql', 'host'),
	config.get('mysql', 'user'),
	config.get('mysql', 'pass'),
	config.get('mysql', 'db'))
cur = dbh.cursor(MySQLdb.cursors.DictCursor)

if message_count == 0:
	cur.execute("SELECT * FROM proxy")
	rows = cur.fetchall()
	for row in rows:
		channel.basic_publish(
				exchange='',
				routing_key=queue_name,
				body=json.dumps(row),
				properties=pika.BasicProperties(
					delivery_mode=2))
		print " [x] Sent %s:%s@%s:%s" % (row['username'], row['password'], row['host'], row['port'])
else:
	msg = " [!] There is %s jobs left in queue" % message_count
	print msg

	msg = MIMEText(msg)
	msg['Subject'] = '[Checker][Fail] Create check proxy jobs'
	msg['From'] = config.get('smtp', 'user')
	msg['To'] = config.get('smtp', 'to')
	smtp = smtplib.SMTP('smtp.gmail.com', 587)
	smtp.ehlo()
	smtp.starttls()
	smtp.ehlo()
	smtp.login(config.get('smtp', 'user'), config.get('smtp', 'pass'))
	smtp.sendmail(config.get('smtp', 'user'), config.get('smtp', 'to'), msg.as_string())
	smtp.close()

# Close connections
rabbit.close()
dbh.close()

