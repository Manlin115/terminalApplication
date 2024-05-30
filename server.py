from flask import Flask, render_template, request
from flask_socketio import SocketIO, send, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    print(f'New connection: {request.sid}')

@socketio.on('disconnect')
def handle_disconnect():
    print(f'Disconnection: {request.sid}')

@socketio.on('message')
def handle_message(data):
    msg = data['message']
    username = data['username']
    print(f'{username}: {msg}')
    send({'message': msg, 'username': username}, broadcast=True)

@socketio.on('join')
def handle_join(data):
    username = data['username']
    print(f'{username} joined')
    send({'message': f'{username} joined', 'username': 'User'}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
