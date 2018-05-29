from flask_restful import Resource, fields, reqparse, marshal_with, abort
from flask import request
from models import db, User, ChatRoom, Message
# from auth import auth

user_fields = {
	'username': fields.String,
}

chatroom_fields = {
	'name': fields.String,
	'creator': fields.String
}

message_fields = {
	'creator': fields.String,
	'text': fields.String,
	'chatroom': fields.String,
}

user_parser = reqparse.RequestParser(bundle_errors=True)
user_parser.add_argument('username', type=str, required=True, location='json')
user_parser.add_argument('password', type=str, required=True, location='json')

chatroom_parser = reqparse.RequestParser(bundle_errors=True)
chatroom_parser.add_argument('name', type=str, required=True, location='json')
chatroom_parser.add_argument('creator', type=str, required=True, location='json')

message_parser = reqparse.RequestParser(bundle_errors=True)
message_parser.add_argument('creator', type=str, required=True, location='json')
message_parser.add_argument('text', type=str, required=True, location='json')
message_parser.add_argument('chatroom', type=str, required=True, location='json')

class UserResource(Resource):
    # @auth.login_required
    @marshal_with(user_fields)
    def get(self, username):
        user = User.query.filter_by(username=username).first()

        if not user:
            abort(404, "User %s: not found." % username)

        return user

    # @auth.login_required
    def delete(self, username):
        user = User.query.filter_by(username=username).first()

        if not user:
            abort(404, "User %s: not found." % username)

        db.session.delete(user)
        db.session.commit()

        return {}, 204

    # @auth.login_required
    @marshal_with(user_fields)
    def put(self, username):
        user = User.query.filter_by(username=username).first()

        if not user:
            abort(404, "User %s: not found." % username)

        password_parser = reqparse.RequestParser()
        password_parser.add_argument('password', type=str, required=True, location='json')

        password_arg = password_parser.parse_args()

        user.password_hash = User.hash_password(password_arg['password'])

        db.session.commit()

        return user

class UserListResource(Resource):
    # @auth.login_required
    @marshal_with(user_fields)
    def get(self):
        users = User.query.all()

        return users

    # @auth.login_required
    @marshal_with(user_fields)
    def post(self):
        user_args = user_parser.parse_args()

        user = User(username=user_args['username'], password_hash=User.hash_password(user_args['password']))

        db.session.add(user)
        db.session.commit()

        return user, 201

class ChatRoomResource(Resource):
    # @auth.login_required
    @marshal_with(chatroom_fields)
    def get(self, name):
        chatroom = ChatRoom.query.filter_by(name=name).first()

        if not chatroom:
            abort(404, "Chatroom %s: not found." % name)

        return chatroom

    # @auth.login_required
    def delete(self, name):
        chatroom = ChatRoom.query.filter_by(name=name).first()

        if not chatroom:
            abort(404, "Chatroom %s: not found." % name)
        # messages = Message.query.filter_by(chatroom=name).all()

        db.session.delete(chatroom)

        db.session.commit()

        return {}, 204

    # @auth.login_required
    # @marshal_with(chatroom_fields)
    # def put(self, name):
        # chatroom = ChatRoom.query.filter_by(name=name).first()

        # if not chatroom:
            # abort(404, "Chatroom %s: not found." % name)

        # db.session.commit()

        # return chatroom

class ChatRoomListResource(Resource):
    # @auth.login_required
    @marshal_with(chatroom_fields)
    def get(self):
        chatrooms = ChatRoom.query.all()

        return chatrooms

    # @auth.login_required
    @marshal_with(chatroom_fields)
    def post(self):
        chatroom_args = chatroom_parser.parse_args()

        chatroom = ChatRoom(name=chatroom_args['name'])
        creator = User.query.filter_by(username=chatroom_args['creator']).first()
        creator.created_rooms.append(chatroom)

        db.session.add(chatroom)
        db.session.commit()

        return chatroom, 201

class MessageResource(Resource):
    # @auth.login_required
    @marshal_with(message_fields)
    def get(self, id):
        message = Message.query.filter_by(id=id).first()

        if not message:
            abort(404, "Message %s: not found." % id)

        return message

    # @auth.login_required
    def delete(self, id):
        message = Message.query.filter_by(id=id).first()

        if not message:
            abort(404, "Message %s: not found." % id)

        db.session.delete(message)
        db.session.commit()

        return {}, 204

    # @auth.login_required
    # @marshal_with(message_fields)
    # def put(self, id):
        # message = Message.query.filter_by(name=name).first()

        # if not message:
            # abort(404, "Message %s: not found." % name)

        # db.session.commit()

        # return chatroom

class MessageListResource(Resource):
    # @auth.login_required
    @marshal_with(message_fields)
    def get(self, chatroom):
        chatroomName = chatroom.replace("%20", " ")
        # messages = Message.query.filter_by(chatroom=chatroomName).all()
        room = ChatRoom.query.filter_by(name=chatroomName).first()

        if not room:
            return {}

        # print(lasttime)
        # print(room.messages.first().posttime)

        return room.messages.all()

    # @auth.login_required
    @marshal_with(message_fields)
    def post(self, chatroom):
        message_args = message_parser.parse_args()

        message = Message(creator=message_args['creator'], text=message_args['text'], chatroom=message_args['chatroom'])

        db.session.add(message)
        db.session.commit()

        return message, 201

# class MessageHistoryResource(Resource):
#     @marshal_with(message_fields)
#     def get(self, chatroom):
#         chatroomName = chatroom.replace("%20", " ")
#         # messages = Message.query.filter_by(chatroom=chatroomName).all()
#         room = ChatRoom.query.filter_by(name=chatroomName).first()
#
#         if not room:
#             return {}
#
#         return room.messages.all()
