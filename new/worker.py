#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pika
import time
import datetime
import json
import sys
from utils.check import check

proxy = None
if len(sys.argv) > 1:
    proxy = sys.argv[1]

max_retries = 3
queue = 'checker'

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue=queue, durable=True)

print '[*] Waiting for messages. To exit press CTRL+C'

def callback(ch, method, properties, body):
    data = json.loads(body)
    print "[>] %s - %s received (try: %d)" % (data.get('keyword'), data.get('domain'), 1 + int(properties.priority))

    if properties.priority >= max_retries:
        ch.basic_ack(delivery_tag=method.delivery_tag)
        print "[!] %s - %s rejected after %d retries" % (data.get('keyword'), data.get('domain'), int(properties.priority))
    else:
        try:
            position = check(data.get('keyword'), data.get('domain'), proxy);
            #TODO: save result to database

            ch.basic_ack(delivery_tag=method.delivery_tag)
            print "[+] Done, position is: %s" % str(position)

        except Exception as err:
            print "Error: %s" % err
            timestamp = time.time()
            now = datetime.datetime.now()
            expire = 1000 * int((now.replace(hour=23, minute=59, second=59, microsecond=999999) - now).total_seconds())
            channel.basic_publish(
                exchange='',
                routing_key=queue,
                body=body,
                properties=pika.BasicProperties(
                    delivery_mode=2,
                    priority=int(properties.priority) + 1,
                    timestamp=timestamp,
                    expiration=str(expire)
                )
            )
            ch.basic_ack(delivery_tag=method.delivery_tag)
            #TODO: notify by email
            if len(err.args) > 1 and '503' in err.args[1]:
                print "[!] Got captcha, going to sleep for 15 min"
                time.sleep(15 * 60)
            else:
                time.sleep(5)

    print

channel.basic_qos(prefetch_count=1)
channel.basic_consume(callback, queue=queue)

try:
    channel.start_consuming()
except KeyboardInterrupt:
    channel.stop_consuming();

connection.close()