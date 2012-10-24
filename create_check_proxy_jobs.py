#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import pika
import sys
import MySQLdb
import ConfigParser
import json
import mail

# Read config.ini
config = ConfigParser.ConfigParser()
config_path = os.path.realpath(
    os.path.join(os.getcwd(),
    os.path.dirname(__file__),
    'config.ini'))
config.read(config_path)

# Connect to RabbitMQ
queue_name = 'proxy_check'
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
	mail.send('marchenko.alexandr@gmail.com', '[Checker][Fail] Create check proxy jobs', msg)

# Close connections
rabbit.close()
dbh.close()

