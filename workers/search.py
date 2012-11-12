#!/usr/bin/env python
import pika
import time
import sys
import json
import ConfigParser
from google import google

# Retrieve auth params for RabbitMQ
cfg = ConfigParser.ConfigParser()
cfg.read('/etc/supervisor/supervisord.conf')
username = cfg.get('inet_http_server', 'username')
password = cfg.get('inet_http_server', 'password')

q = 'google'
proxy = None
if len(sys.argv) > 1:
    proxy = sys.argv[1]

# Connect to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(
    #host='localhost',
    #port=5672,
    #virtual_host='/',
    credentials=pika.credentials.PlainCredentials(
        username=username,
        password=password
    )
))

channel = connection.channel()
channel.queue_declare(queue=q, durable=True)

print " [*] Waiting for job. To exit press CTRL+C"

def callback(ch, method, properties, body):
    data = json.loads(body)
    print " [x] Received %s" % data.keyword
    for page in range(1, 11):
        response = google(data.keyword, page, data.language, data.country, proxy, args.ua, args.cookie, True)
        data.responses.append(response)

    data = retries + 1

    if body == 'mac':
        retries = retries + 1
        print " [%s][!] BAD REQUEST %d" % (worker, retries)
        if retries < 4:
            print " [%s][*] Recreating job" % (worker,)
            data = json.dumps({'body': body, 'retries': retries})
            channel.basic_publish(
                exchange='',
                routing_key=q,
                body=data,
                properties=pika.BasicProperties(
                    delivery_mode = 2 # make message persistent
                )
            )
            print " [%s][*] Goint to sleep" % (worker,)
            time.sleep(5)
            print " [%s][x] Done" % (worker,)
        else:
            print " [%s][!] TOO MANY RETRIES" % (worker,)
    else:
        time.sleep(len(data.get('body')))
        print " [%s][x] Done" % (worker,)
    ch.basic_ack(delivery_tag = method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(callback, queue=q)
channel.start_consuming()
