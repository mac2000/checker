#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import pika
import time
import datetime
from utils.db import get_all_keyword_domain_ids

def send_all():
    ids = get_all_keyword_domain_ids()

    queue = 'checker'

    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue=queue, durable=True)

    for keywords_domains_id in ids:
        timestamp = time.time()
        now = datetime.datetime.now()
        expire = 1000 * int((now.replace(hour=23, minute=59, second=59, microsecond=999999) - now).total_seconds())

        channel.basic_publish(
            exchange='',
            routing_key=queue,
            body=str(keywords_domains_id),
            properties=pika.BasicProperties(
                delivery_mode=2,
                priority=0,
                timestamp=timestamp,
                expiration=str(expire)
            )
        )
        print "[>] %d sent to queue" % keywords_domains_id

    connection.close()

if __name__ == "__main__":
    send_all()