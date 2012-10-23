#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pika
import sys

def get_connection(cfg):
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=cfg.get('rabbitmq', 'host'),
        port=int(cfg.get('rabbitmq', 'port')),
        credentials=pika.PlainCredentials(
            cfg.get('rabbitmq', 'user'),
            cfg.get('rabbitmq', 'pass')
            )
        ))
    return connection


def queue_size(name, cfg, connection):
    channel = connection.channel()
    try:
        queue = channel.queue_declare(queue=name, passive=True)
        return queue.method.message_count
    except:
        return 0
