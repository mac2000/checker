#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pika
import time
import datetime
import json
import sys
import MySQLdb
from utils.check import check
from utils.notify import notify
from utils.db import get_keyword_domain_by
from utils.db import save_search_result

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
    keywords_domains_id = body
    print "[>] %s received (try: %d)" % (keywords_domains_id, 1 + int(properties.priority))

    data = get_keyword_domain_by(keywords_domains_id)

    if not data:
        print "[!] %s not found - skipping" % keywords_domains_id
        ch.basic_ack(delivery_tag=method.delivery_tag)

    else:
        print "[+] %s -> %s - %s" % (keywords_domains_id, data.get('keyword'), data.get('domain'))

        if properties.priority >= max_retries:
            ch.basic_ack(delivery_tag=method.delivery_tag)
            print "[!] %s rejected after %d retries" % (keywords_domains_id, int(properties.priority))
        else:
            try:
                position = check(data.get('keyword'), data.get('domain'), proxy);
                save_search_result(keywords_domains_id, position)
                ch.basic_ack(delivery_tag=method.delivery_tag)
                print "[+] %s done, position is: %s" % (keywords_domains_id, str(position))

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
                #TODO: notify(gmail_from, to, subject, body, gmail_smtp_password)
                if len(err.args) > 1 and '503' in err.args[1]:
                    print "[!] Got captcha, going to sleep for 15 min"
                    #TODO: notify by email
                    #TODO: notify(gmail_from, to, subject, body, gmail_smtp_password)
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