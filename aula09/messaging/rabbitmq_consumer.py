import json
import logging
import threading

import pika
from pika.exceptions import AMQPConnectionError

from config.settings import settings

logger = logging.getLogger("fastapi")


class RabbitMQConsumer:
    def __init__(self, host: str, queue: str, username: str, password: str):
        self.host = host
        self.queue = queue
        self.username = username
        self.password = password
        self.connection = None
        self.channel = None

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

    def callback(self, ch, method, properties, body):
        message = json.loads(body)
        logger.info("Received message: %s", message)
        print("Received message: %s", message)

        ch.basic_ack(delivery_tag=method.delivery_tag)

    def consume(self):
        logger.info("Consuming messages from RabbitMQ")
        self.connect()
        self.channel.basic_consume(queue=self.queue, on_message_callback=self.callback)
        logger.info("Waiting for messages. To exit press CTRL+C")
        try:
            self.channel.start_consuming()
        except KeyboardInterrupt:
            logger.info("Interrupted by user")
            self.close()

    def close(self):
        if self.connection and not self.connection.is_closed:
            self.connection.close()
            logger.info("Connection to RabbitMQ closed")


def start_consumer():
    consumer = RabbitMQConsumer(
        host=settings.RABBITMQ_HOST,
        username=settings.RABBITMQ_DEFAULT_USERNAME,
        password=settings.RABBITMQ_DEFAULT_PASSWORD,
        queue=settings.RABBITMQ_USER_QUEUE
    )
    consumer.consume()


consumer_thread = threading.Thread(target=start_consumer, daemon=True)
