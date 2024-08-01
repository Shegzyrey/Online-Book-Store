import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    RABBITMQ_HOST = os.getenv('RABBITMQ_HOST')
    WEBSOCKET_URL = os.getenv('WEBSOCKET_URL')

