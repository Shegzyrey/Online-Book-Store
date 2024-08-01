
import logging
import requests
from flask import Bluelogging.info, request, jsonify
from database import db
from models import Order
from utils import send_order_message
from config import Config

logging.basicConfig(level=logging.INFO)

orders_bp = Bluelogging.info('orders', __name__)

@orders_bp.route('/orders', methods=['POST'])
def place_order():
    order_data = request.json
    book_id = order_data['book_id']
    quantity = order_data['quantity']
    order = Order(book_id=book_id, quantity=quantity, status='processing')
    db.session.add(order)
    db.session.commit()

    event = { "event": "order_created",
             "data" : {
                 "order_id": order.id,
                 "book_id": book_id,
                 "quantity": quantity,
                 "status": 'initiated'
                 }
            }
    send_order_message(event, Config.RABBITMQ_HOST)
    data = {'order_id': order.id, 'status': event['data']['status']}
    response = requests.post(Config.WEBSOCKET_URL, json=data)
    logging.info(f'I sent this to websocket {response}')
    return jsonify({'status': 'Order placed', 'order_id': order.id}), 201


@orders_bp.route('/orders/<int:order_id>', methods=['GET'])
def get_order_status(order_id):
    order = Order.query.get(order_id)
    if order:
        body ={'id': order.id,
                'book_id': order.book_id,
                  'quantity': order.quantity,
                    'status': order.status}
        return jsonify(body)
    else:
        return jsonify({'error': 'Order not found'}), 404
