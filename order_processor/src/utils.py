import os
import json
import pika
import logging

logging.basicConfig(level=logging.INFO)

def send_stock_update_message(stock_data, rabbitmq_host):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host))
    channel = connection.channel()
    channel.queue_declare(queue='stock_queue')
    channel.basic_publish(exchange='', routing_key='stock_queue', body=json.dumps(stock_data))
    connection.close()
    logging.info(f"Stock update message sent: {stock_data}")

