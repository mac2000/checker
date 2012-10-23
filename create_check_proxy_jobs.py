#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pika
import sys
import MySQLdb

# Connect to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(
	host='localhost',
	port=5672,
	credentials=pika.PlainCredentials(
		'guest',
		'guest'
	)
))

# Get jobs count that are still in queue
message_count = 0
try:
	channel = connection.channel()
	queue = channel.queue_declare(queue=name, passive=True)
	message_count = queue.method.message_count
# If there is no jobs in queue - all ok, create new jobs
	if message_count == 0:
		con = MySQLdb.connect('localhost', 'checker', '3607885', 'checker')
		with con:
			cur = con.cursor(MySQLdb.cursors.DictCursor)
			cur.execute("SELECT * FROM proxy")
			rows = cur.fetchall()
			#TODO: Connect to db and retrieve proxies
			#TODO: create job for each proxy
			print 'going create jobs'
# Otherwise - notify, but only once per day
	else:
		print 'there is still jobs, notify if already not'

except:
	pass
	#TODO: something wrong, send message
finally:
	connection.close()

