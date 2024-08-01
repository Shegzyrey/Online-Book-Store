import pika
import json

def callback(ch, method, properties, body, app, db, Book):
    message = json.loads(body)
    if message['event'] == 'stock_update':
        with app.app_context():
            book_id = message["data"]['book_id']
            stock = message["data"]['stock']
            book = db.session.get(Book, book_id)
            book.stock = stock
            db.session.commit()

def start_consuming(rabbitmq_host, app, db, Book):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host))
    channel = connection.channel()
    channel.queue_declare(queue='update_stock_queue')
    channel.basic_consume(queue='update_stock_queue', on_message_callback=lambda ch, method, properties, body: callback(ch, method, properties, body, app, db, Book), auto_ack=True)
    
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()
    connection.close()
