from flask import Flask
from config import Config
from database import db

from routes.books import books_bp
from routes.orders import orders_bp
# from routes.summarize import summarize_bp

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

app.register_blueprint(books_bp)
app.register_blueprint(orders_bp)
# app.register_blueprint(summarize_bp)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000)
