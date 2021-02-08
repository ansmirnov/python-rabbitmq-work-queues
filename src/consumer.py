#!/usr/bin/env python
import os
import time

import pika

RABBITMQ_HOST = os.environ.get("RABBITMQ_HOST")
RABBITMQ_USER = os.environ.get("RABBITMQ_USER")
RABBITMQ_PASSWORD = os.environ.get("RABBITMQ_PASSWORD")

RABBITMQ_QUEUE = os.environ.get("RABBITMQ_QUEUE")
RABBITMQ_DURABLE = bool(os.environ.get("RABBITME_DURABLE"))

RABBITMQ_PREFETCH_COUNT = int(os.environ.get("RABBITMQ_PREFETCH_COUNT"))

credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=RABBITMQ_HOST, credentials=credentials)
)

channel = connection.channel()

channel.queue_declare(queue=RABBITMQ_QUEUE, durable=RABBITMQ_DURABLE)

def callback(ch, method, properties, body):
    print("Received %r" % body)
    time.sleep(body.count(b'.'))
    print("Done")
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=RABBITMQ_PREFETCH_COUNT)

channel.basic_consume(queue=RABBITMQ_QUEUE, on_message_callback=callback)

channel.start_consuming()
