#!/usr/bin/env python
import os
import sys

import pika

RABBITMQ_HOST = os.environ.get("RABBITMQ_HOST")
RABBITMQ_USER = os.environ.get("RABBITMQ_USER")
RABBITMQ_PASSWORD = os.environ.get("RABBITMQ_PASSWORD")

RABBITMQ_QUEUE = os.environ.get("RABBITMQ_QUEUE")
RABBITMQ_DURABLE = bool(os.environ.get("RABBITME_DURABLE"))

RABBITMQ_DELIVERY_MODE = int(os.environ.get("RABBITMQ_DELIVERY_MODE"))

credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=RABBITMQ_HOST, credentials=credentials)
)

channel = connection.channel()

channel.queue_declare(queue=RABBITMQ_QUEUE, durable=RABBITMQ_DURABLE)

message = ' '.join(sys.argv[1:]) or "Hello World!"

channel.basic_publish(
    exchange='',
    routing_key=RABBITMQ_QUEUE,
    body=message,
    properties=pika.BasicProperties(
        delivery_mode=RABBITMQ_DELIVERY_MODE,
    ))

connection.close()
