import os
import json
import logging
import pika
import requests
from flask import current_app as app
from src.models import Order
from src import db
from src.utils import send_stock_update_message


rabbitmq_host = app.config['RABBITMQ_HOST']
websocket_url = app.config['WEBSOCKET_URL']

logging.basicConfig(level=logging.INFO)

def handle_order_created(event):
    order = Order(
        id=event["data"]['order_id'],
        book_id=event["data"]['book_id'],
        quantity=event["data"]['quantity'],
        status=event["data"]['status']
    )

    db.session.add(order)
    db.session.commit()
    logging.info(f"Order created with ID: {event['data']['order_id']}")



def handle_order_updated(event):
    order_id = event["data"]['order_id']
    order = db.session.query(Order).filter_by(id=order_id).first()

    if order:
        # Update existing order
        order.book_id = event["data"]['book_id']
        order.quantity = event["data"]['quantity']
        order.status = event["data"]['status']

    if order.status == 'failed':
        order.status = 'failed'
    
    db.session.commit()
    logging.info(f"Order processed with ID: {order_id}")


def callback(ch, method, properties, body, websocket_url, rabbitmq_host):
    message = json.loads(body)
    m_event = message['event'] 
    message_status = message['data']['status']
    
    if m_event == 'order_created' and message_status == 'initiated':
        with app.app_context():
            handle_order_created(message)

        with app.app_context():
            order_id = message["data"]['order_id']
            order = db.session.get(Order, order_id)
            book_id = order.book_id
            quantity = order.quantity
            order.status = 'processed'
            db.session.commit()
            data = {'order_id': order.id, 'status': order.status}
            response = requests.post(websocket_url, json=data)
            logging.info(f'I sent this to websocket {response}')

        event = {
            "event": "stock_update",
            "data": {
                'book_id': book_id,
                'quantity': quantity,
                'order_id': order.id
                }
            }

        send_stock_update_message(event, rabbitmq_host)
        logging.info(f"Processed order {event['data']['order_id']}")
    handle_order_updated(message)
    logging.info(f"Processed order {message['data']['order_id']}")
    

def start_consuming():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host))
    channel = connection.channel()
    channel.queue_declare(queue='order_queue')
    channel.basic_consume(
        queue='order_queue', 
        on_message_callback=lambda ch, method, properties, body: callback(ch, method, properties, body, websocket_url, rabbitmq_host), 
        auto_ack=True
    )
    
    logging.info('Waiting for messages...')
    channel.start_consuming()
