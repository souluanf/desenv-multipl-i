import json
import logging

import pika
from pika.exceptions import AMQPConnectionError

logger = logging.getLogger("fastapi")


class RabbitMQProducer:
    def __init__(self, host='localhost', queue='user_events', username='admin', password='admin'):
        self.host = host
        self.queue = queue
        self.username = username
        self.password = password
        self.connection = None
        self.channel = None
        self.connect()

    def connect(self):
        try:
            credentials = pika.PlainCredentials(self.username, self.password)
            parameters = pika.ConnectionParameters(host=self.host, credentials=credentials)
            self.connection = pika.BlockingConnection(parameters)
            self.channel = self.connection.channel()
            self.channel.queue_declare(queue=self.queue, durable=True)
            logger.info("Connected to RabbitMQ")
        except AMQPConnectionError as e:
            logger.error("Failed to connect to RabbitMQ: %s", e)
            raise e

    def publish(self, message):
        try:
            self.channel.basic_publish(
                exchange='',
                routing_key=self.queue,
                body=json.dumps(message).encode(),
                properties=pika.BasicProperties(delivery_mode=2))
            logger.info("Published message to RabbitMQ: %s", message)
        except Exception as e:
            logger.error("Failed to publish message: %s", e)

    def close(self):
        if self.connection and not self.connection.is_closed:
            self.connection.close()
            logger.info("Connection to RabbitMQ closed")
