import logging
import requests
from flask import Flask,request, jsonify
from flask_socketio import SocketIO, emit

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")


@app.route('/')
def index():
    return jsonify({'message': "WebSocket Server is running!"}), 200


@socketio.on('connect')
def handle_connect():
    logging.info('Client connected')
    emit('message', {'message': 'Hello from WebSocket server!'})

@socketio.on('disconnect')
def handle_disconnect():
    logging.info('Client disconnected')


@app.route('/send_update', methods=['POST'])
def send_update():
    data = request.json
    socketio.emit('update', f'{data} was found')
    return jsonify({'status': 'update broadcasted'})


if __name__ == '__main__':
    logging.info('Starting WebSocket server')
    socketio.run(app, host='0.0.0.0', port=5010)
