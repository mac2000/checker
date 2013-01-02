#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import pika
import time
import datetime
import json
import sys

def send(keyword, domain):
    queue = 'checker'

    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue=queue, durable=True)

    timestamp = time.time()
    now = datetime.datetime.now()
    expire = 1000 * int((now.replace(hour=23, minute=59, second=59, microsecond=999999) - now).total_seconds())

    data = {
        'keyword': keyword,
        'domain': domain
    }

    channel.basic_publish(
        exchange='',
        routing_key=queue,
        body=json.dumps(data),
        properties=pika.BasicProperties(
            delivery_mode=2,
            priority=0,
            timestamp=timestamp,
            expiration=str(expire)
        )
    )
    print "[>] %s - %s sent to queue" % (keyword, domain)

    connection.close()

if __name__ == "__main__":
    import argparse
    import re
    parser = argparse.ArgumentParser(description = 'Send job')
    parser.add_argument('keyword', help = 'Keyword to search')
    parser.add_argument('domain', help = 'Domain to search')
    args = parser.parse_args()
    if 'http' in args.domain or 'www.' in args.domain:
        parser.error('Wrong domain given. Do not use "http://" or "www."')

    send(args.keyword, args.domain)