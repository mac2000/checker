#!/usr/bin/env python
import pika
import sys
import json

q = 'test'
msg = ' '.join(sys.argv[1:]) or 'Hello World!'

connection = pika.BlockingConnection(pika.ConnectionParameters(
    #host='localhost',
    #port=5672,
    #virtual_host='/',
    credentials=pika.credentials.PlainCredentials(
        username='guest',
        password='guest'
    )
))

channel = connection.channel()
channel.queue_declare(queue=q, durable=True)

data = json.dumps({'body': msg, 'retries': 0})
channel.basic_publish(
    exchange='',
    routing_key=q,
    body=data,
    properties=pika.BasicProperties(
        delivery_mode = 2 # make message persistent
    )
)

print " [x] Sent %r" % (msg,)
connection.close()
