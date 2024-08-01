import pika
import json
import openai

def create_inventory_message(event, rabbitmq_host):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host))
    channel = connection.channel()
    channel.queue_declare(queue='create_book_queue')
    channel.basic_publish(exchange='', routing_key='create_book_queue', body=json.dumps(event))
    connection.close()

def send_order_message(order_data, rabbitmq_host):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host))
    channel = connection.channel()
    channel.queue_declare(queue='order_queue')
    channel.basic_publish(exchange='', routing_key='order_queue', body=json.dumps(order_data))
    connection.close()

def get_book_summary(book_text, api_key):
    openai.api_key = api_key
    response = openai.Completion.create(
        engine="davinci",
        prompt=f"Summarize the following book:\n\n{book_text}",
        max_tokens=100
    )
    return response.choices[0].text.strip()
