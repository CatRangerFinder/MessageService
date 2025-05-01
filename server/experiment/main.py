import eventlet
eventlet.monkey_patch()

from flask import Flask, render_template, request, session, redirect, url_for
from flask_socketio import join_room, leave_room, send, SocketIO
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import random
from string import ascii_uppercase
from auth import check_password, get_userid


app = Flask(__name__)
app.config['SECRET_KEY'] = 'rwohirrepfnbhfiwepibv'
socketio = SocketIO(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

rooms = {}


def generate_unique_code(length):
    while True:
        code = ""
        for _ in range(length):
            code += random.choice(ascii_uppercase)

        if code not in rooms:
            break

    return code


## Login functions are all here
# User class to handle user data
class User(UserMixin):
    def __init__(self, user_id, username):
        self.id = user_id
        self.username = username


# Load user from the session
@login_manager.user_loader
def load_user(user_id):
    username = session.get('username')
    if user_id and username:
        return User(user_id, username)
    return None


## All the web pages
# Load the main page
@app.route('/')
def main():
    return render_template("main.html")


# Load the login page and logic when somebody requests login
@app.route('/login', methods=["POST", "GET"])
def login():
    # Get the "next" argument in the URL (where the user was trying to go)
    next_page = request.args.get("next")

    if request.method == "POST":
        username = request.form.get("login_username")
        password = request.form.get("login_password")

        # Check if username and password is filled
        if not username or not password:
            return render_template("login.html", error="Please enter Username and Password.")

        # Check if the user exists in the database
        if check_password(username, password):
            user_id = get_userid(username)

            # Store both user_id and username in the session
            session['username'] = username
            session['user_id'] = user_id

            user = User(user_id, username)
            login_user(user)
            return redirect(next_page or url_for("main"))

        else:
            return render_template("login.html", error="Password or Username was incorrect.")

    return render_template("login.html")


# Loads a page to logout and sends them to the main page afterward
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("main"))


# Load the homepage
@app.route('/home')
@login_required  # Protect this page so only logged-in users can access it
def homepage():
    return render_template("home.html")


# Load page to join chat rooms
@app.route('/joinroom', methods=["POST", "GET"])
@login_required
def joinroom():
    if request.method == "POST":
        code = request.form.get("join_code")
        if code not in rooms:
            print(f"room with code: {code} does not exist")
            return render_template("joinroom.html")
        session["room"] = code
        return redirect(url_for("chatroom"))

    return render_template("joinroom.html")


# Load page to create chat rooms
@app.route('/createroom', methods=["POST", "GET"])
@login_required
def createroom():
    if request.method == "POST":
        room = generate_unique_code(4)
        rooms[room] = {"members": 0, "messages": []}
        session["room"] = room
        return redirect(url_for("chatroom"))

    return render_template("createroom.html")


@app.route("/room")
def chatroom():
    room = session.get("room")
    if room is None or session.get("username") is None or room not in rooms:
        return redirect(url_for("main"))

    return render_template("chatroom.html", room=room)


@socketio.on("connect")
def connect(auth):
    room = session.get("room")
    username = session.get("username")
    if not room or not username:
        return
    if room not in rooms:
        leave_room(room)
        return

    join_room(room)
    send({"username": "SYSTEM", "message": f"{username} has entered the room"}, to=room)
    rooms[room]["members"] += 1
    print(f"{username} joined room {room}")


@socketio.on("disconnect")
def disconnect():
    room = session.get("room")
    username = session.get("username")
    leave_room(room)

    if room in rooms:
        rooms[room]["members"] -= 1
        if rooms[room]["members"] <= 0:
            del rooms[room]

    send({"username": "SYSTEM", "message": f"{username} has left the room"}, to=room)
    print(f"{username} has left the room {room}")


@socketio.on("send_message")
def handle_message(data):
    room = session.get("room")
    username = session.get("username")
    if room and room in rooms:
        message = data["message"]
        # Broadcast the message to everyone in the room
        send({"username": username, "message": message}, to=room)
        print(f"Message from {username}: {message}")


if __name__ == '__main__':
    print("server running")
    socketio.run(app, host="0.0.0.0", port=5000, debug=False)
    #socketio.run(app, async_mode='eventlet')
    #socketio.run(app, debug=False, use_reloader=False)#, server='eventlet')
