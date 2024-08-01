import socketio
import logging

logging.basicConfig(level=logging.INFO)

sio = socketio.Client()

@sio.event
def connect():
    logging.info('Connection established')

@sio.event
def disconnect():
    logging.info('Disconnected from server')

@sio.event
def message(data):
    logging.info(f'Received message: {data}')

@sio.on('update')
def on_update(data):
    logging.info(f'Update received: {data}')

if __name__ == '__main__':
    sio.connect('http://websocket:5010')
    sio.wait()
