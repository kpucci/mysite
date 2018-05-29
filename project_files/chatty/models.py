from flask_sqlalchemy import SQLAlchemy

# Instantiate a database object
db = SQLAlchemy()

# One user creates many rooms
# One room has one creator

# One user joins one room
# One room has many users

# One room has many messages
# One message has one room

users = db.Table('users',
    db.Column('chat_room_name', db.String, db.ForeignKey('chat_room.name')),
    db.Column('user_username', db.String, db.ForeignKey('user.username'))
)

rooms = db.Table('rooms',
    db.Column('user_username', db.String, db.ForeignKey('user.username')),
    db.Column('chat_room_name', db.String, db.ForeignKey('chat_room.name'))
)

class User(db.Model):
    username = db.Column(db.String(80), unique = True, primary_key = True)
    password = db.Column(db.String(100))

    created_rooms = db.relationship('ChatRoom', secondary='rooms',lazy='dynamic',backref='creator')

    # curr_room_id = db.Column(db.String, db.ForeignKey('chat_room.name'))
    # curr_room = db.relationship('ChatRoom',secondary='users',backref='users', lazy='dynamic')

    def _repr_(self):
        return "<User {}>".format(repr(self.username))

class ChatRoom(db.Model):
    name = db.Column(db.String(80), unique = True, primary_key = True)
    # creator_id = db.Column(db.String, db.ForeignKey('user.username'))
    # creator = db.relationship('User', backref='rooms', foreign_keys=[creator_id])
    users = db.relationship('User', secondary='users',lazy='dynamic', backref='curr_room')
    messages = db.relationship('Message', backref='chat_room', cascade='delete', lazy='dynamic')

    def _repr_(self):
        return "<ChatRoom {}>".format(repr(self.name))


class Message(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    creator = db.Column(db.String, db.ForeignKey('user.username'))
    text = db.Column(db.String(400))
    chatroom = db.Column(db.String, db.ForeignKey('chat_room.name'))
    posttime = db.Column(db.DateTime)

    def _repr_(self):
    	return "<Message {}>".format(repr(self.name))
