#!/usr/bin/env python
import pika
import time
import sys
import json

q = 'echo'
worker = ' '.join(sys.argv[1:]) or 'test'

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

print " [*] Waiting for messages. To exit press CTRL+C"

def callback(ch, method, properties, body):
    print " [x] Received %s" % body
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
