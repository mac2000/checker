#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import pika
import sys
import MySQLdb
import ConfigParser
import json
import pycurl
import cStringIO
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
			# mail.send('marchenko.alexandr@gmail.com', '[Checker][SUCCESSL] Proxy checked', 'CHECKED')
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
