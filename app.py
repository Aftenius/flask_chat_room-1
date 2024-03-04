from flask import Flask, render_template, session, redirect, url_for, request, Response, abort
from flask_socketio import SocketIO, emit, join_room, leave_room, send
from pathlib import Path
import requests
import random
import json
from string import ascii_uppercase

import schedule
import threading
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my-secret-key'

socketio = SocketIO(app)

rooms = {}
url = 'https://api.telegram.org/bot6985903476:AAHb_dmARjQXg7lBBqGCJnpBgR07VWEoJmQ/sendMessage'


def background_process():
    while True:
        schedule.run_pending()

        sleep_time = schedule.idle_seconds()

        if sleep_time is not None and sleep_time > 0:
            sleep_time_formatted = time.strftime('%H:%M:%S', time.gmtime(sleep_time))
            print(f"будет спать еще {sleep_time_formatted}")

            # Ожидание до следующей задачи
            time.sleep(sleep_time)
        else:
            print("Задач нет, спать 1 секунду")
            time.sleep(1)


def notification1645():
    with open('users.json', 'r') as file:
        data = json.load(file)

        for tg_id in data:
            print(tg_id['tg_id'])
            message_text = (f'🔔❗️{tg_id["first_name"]}, не забудьте внести трудозатраты за сегодняшний день.\n'
                            f'Сделайте это прямо сейчас в приложении <a href="https://tcs.pesk.spb.ru/auth/login">TaskPesk</a>🔔❗️')
            params = {'chat_id': tg_id['tg_id'], 'text': message_text, 'parse_mode': 'HTML'}  #
            response = requests.post(url, data=params)

    print(123)


schedule.every().day.at("16:45").do(notification1645)


bg_process = threading.Thread(target=background_process)
bg_process.daemon = True
bg_process.start()


lock = threading.Lock()


def add_user(data):
    with lock:
        file_path = Path('users.json')

        if file_path.is_file():
            with open(file_path, 'r', encoding='utf-8') as file:
                users = json.load(file)
        else:
            users = []

        existing_user = next((user for user in users if user['tg_id'] == data['tg_id']), None)
        if existing_user:
            existing_user.update(data)
        else:
            users.append(data)

        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(users, file, ensure_ascii=False, indent=4)


@app.route('/notification', methods=['POST'])
def notification():
    if request.headers.get('content-type') == 'application/json':
        data = request.json

        data = request.json
        message = data['message']

        if 'text' in message:
            print(data)
            content = f"Текст: {message['text']}" + f" id: {message['from']['id']} Name: {message['from']['first_name']}"
            message_text = data['message']['text']
            if message_text.endswith("@pesk.spb.ru"):
                user_id = data['message']['from']['id']
                user_name = data['message']['from']['first_name']
                user_json = {
                    'first_name': user_name,
                    'post_name': 'admin',
                    'email': message_text,
                    'tg_id': user_id
                }

                add_user(user_json)

                mess = f"Спасибо 😊"
                params1 = {'chat_id': data['message']['from']['id'], 'text': mess, 'parse_mode': 'HTML'}
                requests.post(url, data=params1)
                print(message)
            else:
                mess = f"Мне нужна только ваша корпоративная почта.\n\n<i>Я бот для уведомлений, старайся не засорять этот чат.</i>😊"
                params1 = {'chat_id': data['message']['from']['id'], 'text': mess, 'parse_mode': 'HTML'}
                requests.post(url, data=params1)

                print(f"--NO-- {data['message']['from']['id']}")

        elif 'sticker' in message:
            mess = f"Мне нужна только ваша корпоративная почта.\n\n<i>Я бот для уведомлений, старайся не засорять этот чат.</i>😊"
            params1 = {'chat_id': data['message']['from']['id'], 'text': mess, 'parse_mode': 'HTML'}
            requests.post(url, data=params1)
            print(message)

            content = f"Стикер: {message['sticker'].get('emoji', 'Нет эмодзи')}" + f" id: {message['from']['id']} Name: {message['from']['first_name']}"
        elif 'photo' in message:
            mess = f"Мне нужна только ваша корпоративная почта.\n\n<i>Я бот для уведомлений, старайся не засорять этот чат.</i>😊"
            params1 = {'chat_id': data['message']['from']['id'], 'text': mess, 'parse_mode': 'HTML'}
            requests.post(url, data=params1)
            print(message)

            content = "Фото получено" + f" id: {message['from']['id']} Name: {message['from']['first_name']}"
        elif 'video' in message:
            mess = f"Мне нужна только ваша корпоративная почта.\n\n<i>Я бот для уведомлений, старайся не засорять этот чат.</i>😊"
            params1 = {'chat_id': data['message']['from']['id'], 'text': mess, 'parse_mode': 'HTML'}
            requests.post(url, data=params1)

            content = "Видео получено" + f" id: {message['from']['id']} Name: {message['from']['first_name']}"
        elif 'audio' in message:
            mess = f"Мне нужна только ваша корпоративная почта.\n\n<i>Я бот для уведомлений, старайся не засорять этот чат.</i>😊"
            params1 = {'chat_id': data['message']['from']['id'], 'text': mess, 'parse_mode': 'HTML'}
            requests.post(url, data=params1)

            content = "Аудио получено" + f" id: {message['from']['id']} Name: {message['from']['first_name']}"
        elif 'voice' in message:
            mess = f"Мне нужна только ваша корпоративная почта.\n\n<i>Я бот для уведомлений, старайся не засорять этот чат.</i>😊"
            params1 = {'chat_id': data['message']['from']['id'], 'text': mess, 'parse_mode': 'HTML'}
            requests.post(url, data=params1)

            content = "Голосовое сообщение получено" + f" id: {message['from']['id']} Name: {message['from']['first_name']}"
        elif 'document' in message:
            mess = f"Мне нужна только ваша корпоративная почта.\n\n<i>Я бот для уведомлений, старайся не засорять этот чат.</i>😊"
            params1 = {'chat_id': data['message']['from']['id'], 'text': mess, 'parse_mode': 'HTML'}
            requests.post(url, data=params1)

            content = "Документ получен" + f" id: {message['from']['id']} Name: {message['from']['first_name']}"
        elif 'location' in message:
            mess = f"Мне нужна только ваша корпоративная почта.\n\n<i>Я бот для уведомлений, старайся не засорять этот чат.</i>😊"
            params1 = {'chat_id': data['message']['from']['id'], 'text': mess, 'parse_mode': 'HTML'}
            requests.post(url, data=params1)

            content = "Локация получена" + f" id: {message['from']['id']} Name: {message['from']['first_name']}"
        elif 'contact' in message:
            mess = f"Мне нужна только ваша корпоративная почта.\n\n<i>Я бот для уведомлений, старайся не засорять этот чат.</i>😊"
            params1 = {'chat_id': data['message']['from']['id'], 'text': mess, 'parse_mode': 'HTML'}
            requests.post(url, data=params1)

            content = "Контакт получен" + f" id: {message['from']['id']} Name: {message['from']['first_name']}"
        else:
            mess = f"Мне нужна только ваша корпоративная почта.\n\n<i>Я бот для уведомлений, старайся не засорять этот чат.</i>😊"
            params1 = {'chat_id': data['message']['from']['id'], 'text': mess, 'parse_mode': 'HTML'}
            requests.post(url, data=params1)

            content = "Неподдерживаемый тип сообщения" + f" id: {message['from']['id']} Name: {message['from']['first_name']}"

        return Response('ok', status=200)

    else:
        abort(403)


def generate_code(length):
    """ 
    Generate a random code consisting of uppercase ASCII characters of a specified length,
    and return the code. The code is guaranteed to not already exist in the `rooms` list.
    """
    while True:
        code = ''.join(random.choice(ascii_uppercase) for _ in range(length))
        if code not in rooms:
            break
    return code

# Define the home page view for the chat application.
@app.route('/', methods=('GET', 'POST'))
def home_view():
    # Clear the session to start fresh.
    session.clear()

    # If the form is submitted.
    if request.method == 'POST':
        # Get the name and code from the form.
        name = request.form.get('name')
        code = request.form.get('code')

        # Check if the user wants to join or create a room.
        join = request.form.get('join', False)
        create = request.form.get('create', False)

        # Validate the form inputs.
        if not name:
            # If the name is missing, show an error message.
            return render_template('home.html', error_message='Please enter a name.', name=name, code=code)
        elif join != False and not code:
            # If the user wants to join a room but the code is missing, show an error message.
            return render_template('home.html', error_message='Please enter a room code.', name=name, code=code)

        # Set the default room to be the code entered by the user.
        room = code

        # If the user wants to create a room.
        if create != False:
            # Generate a random 6-digit code for the new room.
            room = generate_code(6)
            # Add the new room to the dictionary of rooms.
            rooms[room] = {'members': 0, 'messages': []}
        # If the user wants to join a room but the code is not valid.
        elif code not in rooms:
            # Show an error message.
            return render_template('home.html', error_message='Room does not exist.', name=name, code=code)

        # Store the room code and user name in the session.
        session['room'] = room
        session['name'] = name

        # Redirect the user to the room page.
        return redirect(url_for('room_view'))

    # If the form is not submitted, show the home page.
    return render_template('home.html')
# Define the room page view for the chat application.
@app.route('/room')
def room_view():
    """ 
    defines the view for the chat room page
    It retrieves the room from the session and ensures the user is logged in and the room exists
    If the user is not logged in or the room does not exist, it redirects to the home page
    Otherwise, it renders the room template with the room name and messages for that room.
    """
    # Get the room  from the session 
    room = session.get('room')
    
    if room is None or session.get('name') is None or room not in rooms:
        return redirect(url_for('home_view'))

    return render_template('room.html', room=room, messages=rooms[room]['messages'], members=rooms[room]['members'])

@socketio.on('message')
def handle_message(data):
    # Get the current room and user name from the session
    room = session.get('room')
    name = session.get('name')
    # If the room does not exist return
    if room not in rooms:
        return 
    # Construct the message content
    content = {'name': name, 'message': data['data']}
    # Send the message to all clients in the room
    send(content, to=room)
    # Add the content to the room's message history 
    rooms[room]['messages'].append(content)
    

@socketio.on('connect')
def handle_connect(auth):
    # Get the current room and user name from the session
    room = session.get('room')
    name = session.get('name')

    if not name or not room:
        return 
    elif room not in rooms:
        leave_room(room)
        return 
    # Join the room if does exist
    join_room(room)
    # Send a message to the room indicating that the user has entered
    send({'name': name, 'message': 'has entered the room'}, to=room)
    # Add a member
    rooms[room]['members'] += 1
    
# This function should be called when a client disconnects from the server
@socketio.on('disconnect')
def handle_disconnect():
    # Sessions can be used to store and retrieve data for a specific client.
    # Get the current room and user name from the session
    room = session.get('room')
    name = session.get('name')
    # Check if the room is in the dictionary of active rooms
    if room in rooms:

        # Reduce the member count for the room
        rooms[room]['members'] -= 1
        # If the room has no more members, remove it from the active rooms dictionary
        if rooms[room]['members'] == 0:
            del rooms[room]
    # Send a message to the room indicating that the user has left
    send({'name': name, 'message': 'has left the room'}, to=room)
    

if __name__ == '__main__':

    socketio.run(app, host='localhost', port=8080, allow_unsafe_werkzeug=True, debug=False)


