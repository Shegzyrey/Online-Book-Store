import json
import requests
import os
import logging
import pika
from flask import current_app as app, request
from .models import Book
from . import db
from .utils import send_stock_update_to_api_gateway, send_order_message

rabbitmq_host = app.config['RABBITMQ_HOST']
websocket_url = app.config['WEBSOCKET_URL']

logging.basicConfig(level=logging.INFO)

def handle_book_created(event):
    book = Book(
        id=event["data"]['book_id'],
        title=event["data"]['title'],
        author=event["data"]['author'],
        stock=event["data"]['stock']
    )

    db.session.add(book)
    db.session.commit()
    logging.info(f"Book created with ID: {event['data']['book_id']}")


def handle_stock_update(event):
    book_id = event['data']['book_id']
    book = Book.query.get(book_id)
    if book and book.stock >= event['data']['quantity']:
        book.stock -= event['data']['quantity']
        db.session.commit()
        logging.info(f"Updated stock for book {book_id}")
        send_stock_update_to_api_gateway(book_id, book.stock, rabbitmq_host)
    else:
        order_id = event['data']['order_id']
        data = {'book_id': book_id, 'message': 'not enough stock'}
        event = { "event": "order_created",
                "data" : {
                    "order_id": order_id,
                    "book_id": book_id,
                    "quantity": book.stock,
                    "status": 'failed'
                    }
                }
        send_order_message(event, rabbitmq_host)
        data = {'order_id': order_id, 'status': event['data']['status']}
        response = requests.post(websocket_url, json=data)
        logging.info(response)
        logging.warning(f"Book {book_id} does not exist or not enough stock")


def book_created_callback(ch, method, properties, body):
    message = json.loads(body)
    if message['event'] == 'book_created':
        with app.app_context():
            handle_book_created(message)


def stock_update_callback(ch, method, properties, body):
    message = json.loads(body)
    if message['event'] == 'stock_update':
        with app.app_context():
            handle_stock_update(message)


def start_consuming():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host))
    channel = connection.channel()
    
    channel.queue_declare(queue='create_book_queue')
    channel.queue_declare(queue='stock_queue')
    
    channel.basic_consume(queue='create_book_queue', on_message_callback=book_created_callback, auto_ack=True)
    channel.basic_consume(queue='stock_queue', on_message_callback=stock_update_callback, auto_ack=True)
    
    logging.info('Waiting for messages...')
    channel.start_consuming()
