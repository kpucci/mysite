import os
import datetime
import project_files.chatty.models as models
import project_files.chatty.resources as resources
from sqlalchemy import exc
# import requests
from flask import (
    Flask,
    request,
    abort,
    url_for,
    redirect,
    session,
    render_template,
    flash
)

from flask_restful import (
    reqparse,
    abort,
    Api,
    Resource
)

from project_files.chatty.models import (
    db,
    User,
    ChatRoom,
    Message
)
from project_files.chatty.resources import (
    UserResource,
    UserListResource,
    ChatRoomResource,
    ChatRoomListResource,
    MessageResource,
    MessageListResource
)

app = Flask(__name__)
app.static_folder = 'project_files/chatty/static'
app.template_folder = 'project_files/chatty/templates'
api = Api(app)

app.config.update(dict(
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='owner',
    PASSWORD='pass',

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(app.root_path, 'chat.db')
))

db.init_app(app)

api.add_resource(UserListResource, '/users/')
api.add_resource(UserResource, '/users/<string:username>')
api.add_resource(ChatRoomListResource, '/chatrooms/')
api.add_resource(ChatRoomResource, '/chatrooms/<string:name>')
api.add_resource(MessageListResource, '/messages/<string:chatroom>')
# api.add_resource(MessageHistoryResource, '/history/<string:chatroom>')
# api.add_resource(MessageResource, '/messages/<int:id>')

@app.cli.command('initdb')
def testdb_command():
    db.drop_all()
    db.create_all()

    user1 = User(username='user1', password='pass')
    db.session.add(user1)

    chatroom1 = ChatRoom(name='Super Awesome Chat Room')
    db.session.add(chatroom1)

    user1.created_rooms.append(chatroom1)

    message1 = Message(creator=user1.username,text="Hello, there!", chatroom=chatroom1.name)
    db.session.add(message1)
    db.session.commit()

    print('Initialized the database.')

@app.cli.command('testdb')
def testdb_command():
    db.drop_all()
    db.create_all()

    user1 = User(username='kpucci', password='morton301')
    db.session.add(user1)

    print('User1: %s' % user1.username)

    user2 = User(username='zewl', password='blah')
    db.session.add(user2)

    print('User2: %s' % user2.username)

    chatroom1 = ChatRoom(name='Super Awesome Chat Room')
    print('Chatroom1: %s' % chatroom1.name)
    print(chatroom1.name)
    db.session.add(chatroom1)

    user1.created_rooms.append(chatroom1)

    chatroom1.users.append(user1)


    print(len(user2.curr_room))

    posttime1 = datetime.datetime.now()

    message1 = Message(creator=user1.username,text="Hello, there!", chatroom=chatroom1.name, posttime=posttime1)
    db.session.add(message1)
    db.session.commit()

    print('Message1: %s' % message1.text)



#--------------------------------------------------------------------------------------------

# Home page:
# GET - Visit home page
# POST - Signin --> Redirect to profile page if successful
@app.route("/", methods=['GET'])
def default():
    if "logged_in" in session:
            return redirect(url_for("user_account",username=session.get("logged_in")))
    return render_template("home.html")


#--------------------------------------------------------------------------------------------

# Login page:
# GET - Visit login page
# POST - login --> Redirect to user page if successful
@app.route("/login/", methods=["GET","POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    if request.form["login-button"] == "cancel":
        return redirect(url_for('default'))

    user = User.query.filter((User.username==request.form["username"]) & (User.password==request.form["password"])).first()

    if not user:
        flash('Incorrect username or password')
        return redirect(url_for('login'))

    session['logged_in'] = user.username
    return redirect(url_for("user_account", username=user.username))

#--------------------------------------------------------------------------------------------

# Logouy page:
# GET - Logout
@app.route("/logout/", methods=["GET","POST"])
def logout():
    if "logged_in" in session:
        user = User.query.filter_by(username=session.get("logged_in")).first()
        if len(user.curr_room) != 0:
            room_name = user.curr_room[0].name
            room = ChatRoom.query.filter_by(name=room_name).first()
            room.users.remove(user)
        try:
            db.session.commit()
            session.pop('logged_in', None)
            flash("You've been signed out.")
            return redirect(url_for('default'))
        except exc.SQLAlchemyError:
            flash("There was a problem leaving the chatroom.")
            return redirect(url_for('default'))
    return redirect(url_for('default'))

#--------------------------------------------------------------------------------------------

# Signup page:
# GET - Visit signup page
# POST - Signup --> Redirect to user page if successful
@app.route("/signup/", methods=["GET","POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")

    if request.form["signup-button"] == "cancel":
        return redirect(url_for('default'))

    if request.form["password"] != request.form["password2"]:
        flash("The passwords did not match.")
        return redirect(url_for('signup'))
    elif User.query.filter_by(username=request.form["username"]).scalar() is not None:
        flash("That username has been taken already.")
        return redirect(url_for('signup'))

    newUser = User(username=request.form["username"], password=request.form["password"])
    db.session.add(newUser)
    try:
        db.session.commit()
        session['logged_in'] = newUser.username
        return redirect(url_for('user_account', username=newUser.username))
    except exc.SQLAlchemyError:
        flash("There was a problem creating your account.")
        return redirect(url_for('signup'))

#--------------------------------------------------------------------------------------------

# Account page:
# GET - Visit account page

@app.route("/account/<username>", methods=["GET","POST"])
def user_account(username=None):
    if "logged_in" in session and session.get("logged_in") == username:
        user = User.query.filter_by(username=username).first()
        if request.method == "GET":
            return render_template("account.html", username=user.username)
        else:
            roomname = request.form["join-chat-button"]
            return redirect(url_for('chatroom', room_name=roomname))
    else:
        flash("You don't have access to this account. Please login first.")
        return redirect(url_for('default'))

#--------------------------------------------------------------------------------------------

# Chatroom page:
# GET - Visit chatroom page

@app.route("/room/<room_name>", methods=["GET","POST"])
def chatroom(room_name=None):
    room = ChatRoom.query.filter_by(name=room_name).first()
    if "logged_in" in session:
        user = User.query.filter_by(username=session.get("logged_in")).first()
        # print(len(user.curr_room))
        if len(user.curr_room) == 0:
            room.users.append(user)
            try:
                db.session.commit()
                return render_template("chatroom.html", current_user=user.username, logged_in=True, room_name=room_name, room_creator=room.creator[0].username, message_list=room.messages.all())
            except exc.SQLAlchemyError:
                flash("There was a problem joining this chatroom.")
                return redirect(url_for('user_account', username=user.username))
        else:
            curr_room = user.curr_room[0].name
            if room_name == curr_room:
                return render_template("chatroom.html", current_user=user.username, logged_in=True, room_name=room_name, room_creator=room.creator[0].username)
            flash("You can only join one room at a time.")
            return redirect(url_for('user_account', username=user.username))
    return render_template('chatroom.html', username=None, loggedIn=False, room_name=room_name, message_list=room.messages.all())

#--------------------------------------------------------------------------------------------

# Leave chatroom:
# GET - Visit chatroom page

@app.route("/leave/<room_name>", methods=["GET","POST"])
def leaveChatroom(room_name=None):
    if "logged_in" in session:
        user = User.query.filter_by(username=session.get("logged_in")).first()
        room = ChatRoom.query.filter_by(name=room_name).first()
        room.users.remove(user)
        try:
            db.session.commit()
            return redirect(url_for('user_account', username=user.username))
        except exc.SQLAlchemyError:
            flash("There was a problem leaving this chatroom.")
            return redirect(url_for('user_account', username=user.username))

    return redirect(url_for('default'))


if __name__ == "__main__":
	app.run(debug=True)
