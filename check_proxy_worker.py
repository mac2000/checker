#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pika
import sys
import MySQLdb
import ConfigParser
import json
import pycurl
import cStringIO
import smtplib
from email.mime.text import MIMEText

# Read config.ini
config = ConfigParser.ConfigParser()
config.read('config.ini')

queue_name = 'proxy_check'

# Configure cURL

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
channel.queue_declare(queue=queue_name, durable=True)

def callback(ch, method, properties, body):
	data = json.loads(body)
	print '-------------------------------------------'
	print " [x] Received %s:%s@%s:%s" % (data['username'], data['password'], data['host'], data['port'])
	buf = cStringIO.StringIO()
	c = pycurl.Curl()
	c.setopt(c.URL, 'http://checker.mac-blog.org.ua/ip.php')
	c.setopt(c.VERBOSE, 0)
	c.setopt(c.FAILONERROR, 1)
	c.setopt(c.PROXY, str(data['host']))
	c.setopt(c.PROXYPORT, int(data['port']))
	c.setopt(c.PROXYUSERPWD, '%s:%s' % (str(data['username']), str(data['password'])))
	c.setopt(c.WRITEFUNCTION, buf.write)

	try:
		c.perform()
		ip = buf.getvalue()
		if ip == data['host']:
			print " [+] %s == %s" % (data['host'], ip)
			msg = MIMEText('CHECKED')
			msg['Subject'] = '[Checker][SUCCESSL] Proxy checked'
			msg['From'] = config.get('smtp', 'user')
			msg['To'] = config.get('smtp', 'to')
			smtp = smtplib.SMTP('smtp.gmail.com', 587)
			smtp.ehlo()
			smtp.starttls()
			smtp.ehlo()
			smtp.login(config.get('smtp', 'user'), config.get('smtp', 'pass'))
			smtp.sendmail(config.get('smtp', 'user'), config.get('smtp', 'to'), msg.as_string())
			smtp.close()
		else:
			print " [!] %s != %s" % (data['host'], ip)
			#TODO: stop worker (set flag)
	except pycurl.error, error:
		errno, errstr = error
		print ' [!] %s : %s' % (errno, errstr)
		#TODO: stop worker (set flag)

	buf.close()
	print " [x] Done"
	ch.basic_ack(delivery_tag = method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(callback, queue=queue_name)
channel.start_consuming()
