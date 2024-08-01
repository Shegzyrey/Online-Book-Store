import os
import json
import pika
import logging


def send_stock_update_to_api_gateway(book_id, stock, rabbitmq_host):
    event = {
        "event": "stock_update",
        "data": {'book_id': book_id, 'stock': stock}
    }
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host))
    channel = connection.channel()
    channel.queue_declare(queue='update_stock_queue')
    channel.basic_publish(exchange='', routing_key='update_stock_queue', body=json.dumps(event))
    connection.close()
    logging.info(f"Stock update sent to API Gateway for book {book_id}")


def send_order_message(order_data, rabbitmq_host):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host))
    channel = connection.channel()
    channel.queue_declare(queue='order_queue')
    channel.basic_publish(exchange='', routing_key='order_queue', body=json.dumps(order_data))
    connection.close()