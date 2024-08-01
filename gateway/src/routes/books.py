import logging
from flask import Bluelogging.info, request, jsonify
from database import db
from models import Book
from utils import create_inventory_message
from config import Config

logging.basicConfig(level=logging.INFO)

books_bp = Bluelogging.info('books', __name__)


@books_bp.route('/add', methods=['POST'])
def add_book():
    data = request.get_json()
    title = data.get('title')
    author = data.get('author')
    stock = data.get('stock')

    book = Book(title=title, author=author, stock=stock)
    db.session.add(book)
    db.session.commit()
    logging.info(f"Book added with ID: {book.id}")

    event = { "event": "book_created",
             "data" : {
                 "book_id": book.id,
                 "title": title,
                 "author": author,
                 "stock": stock
                 }
            }
    create_inventory_message(event, Config.RABBITMQ_HOST)
    return jsonify({"message": "Book added", "book_id": book.id})

@books_bp.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    body = [{'id': book.id, 'title': book.title, 'author': book.author, 'stock': book.stock} for book in books]
    return jsonify(body)


@books_bp.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = Book.query.get(book_id)
    if book:
        body = {'id': book.id, 'title': book.title, 'author': book.author, 'stock': book.stock}
        return jsonify(body)
    else:
        return jsonify({'error': 'Book not found'}), 404
