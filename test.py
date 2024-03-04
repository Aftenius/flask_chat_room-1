from datetime import datetime

from flask import Flask, request, jsonify, render_template
from flask_socketio import SocketIO, join_room, emit
from flask_caching import Cache


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['CACHE_TYPE'] = 'SimpleCache'
socketio = SocketIO(app, cors_allowed_origins="http://localhost:3000")
cache = Cache(app)


@app.route('/')
def index():
    return render_template('test.html')


@socketio.on('connect')  # Обработчик события Socket.IO для подключения пользователя
def handle_connect_user(data):
    print('--->Da')
    emit('connected', {'user_id': '123'})


@socketio.on('connect_user')  # Обработчик события Socket.IO для подключения пользователя
def handle_connect_user(data):
    user_id = data.get('user_id')
    join_room(user_id)
    emit('connected', {'user_id': user_id})


@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.json
    room = data.get('name_room')
    message = data.get('message')
    socketio.emit('message', {'message': message}, room=room)
    save_notification(user_id=room, message=message)
    return jsonify({'status': 'message sent', 'room': room, 'message': message})


@app.route('/get_app_notification', methods=['GET'])
def get_app_notification():
    user_id = request.headers.get("User-Id")
    return cache.get(user_id) or []


def save_notification(user_id, message):
    notifications = cache.get(user_id) or []

    notifications.append(message)

    timeout = get_time_end_of_day()
    cache.set(user_id, notifications, timeout=timeout)


def get_time_end_of_day():
    # Вычисляет количество секунд до 23:59 текущего дня.
    now = datetime.now()
    end_of_day = datetime(now.year, now.month, now.day, 23, 59, 50)
    delta = end_of_day - now
    return delta.total_seconds()


if __name__ == '__main__':
    print('=====>')
    socketio.run(app, debug=True)
