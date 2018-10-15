from flask_restful import Resource, fields, reqparse, marshal_with, inputs
from flask import request, abort, flash, jsonify, json
from puckperfect_models import db, Player, Coach, Parent, Drill, Practice, Playlist, Team
from datetime import datetime, timedelta

# NOTE: Marshal fields determine what kind of data is returned
#       from a request
player_fields = {
    'id': fields.Integer,
	'email': fields.String,
    'password': fields.String,
    'first_name': fields.String,
    'last_name': fields.String,
    'hockey_level': fields.Integer,
    'skill_level': fields.Integer,
    'hand': fields.Boolean
}

player_email_fields = {
	'email': fields.String
}

coach_fields = {
    'id': fields.Integer,
	'email': fields.String,
    'password': fields.String,
    'first_name': fields.String,
    'last_name': fields.String
}

parent_fields = {
    'id': fields.Integer,
    'email': fields.String,
    'password': fields.String,
    'first_name': fields.String,
    'last_name': fields.String,
    'child_name': fields.String
}

drill_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'description': fields.String
}

practice_fields = {
    'id': fields.Integer,
    'player_id': fields.Integer,
    'drill_id': fields.Integer,
    'speed': fields.Float
}

playlist_fields = {
    'id': fields.Integer,
    'player_id': fields.Integer
}

team_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'league': fields.String,
    'division': fields.String
}

# NOTE: Parsers determine what kind of data can be sent along with a request (for things like put, post, etc.)
player_parser = reqparse.RequestParser(bundle_errors=True)
player_parser.add_argument('id', type=int, location='json')
player_parser.add_argument('email', type=str, required=True, location='json')
player_parser.add_argument('password', type=str, required=True, location='json')
player_parser.add_argument('first_name', type=str, required=True, location='json')
player_parser.add_argument('last_name', type=str, required=True, location='json')
player_parser.add_argument('hockey_level', type=int, required=True, location='json')
player_parser.add_argument('skill_level', type=int, required=True, location='json')
player_parser.add_argument('hand', type=inputs.boolean, required=True, location='json')

coach_parser = reqparse.RequestParser(bundle_errors=True)
coach_parser.add_argument('id', type=int, location='json')
coach_parser.add_argument('email', type=str, required=True, location='json')
coach_parser.add_argument('password', type=str, required=True, location='json')
coach_parser.add_argument('first_name', type=str, required=True, location='json')
coach_parser.add_argument('last_name', type=str, required=True, location='json')

parent_parser = reqparse.RequestParser(bundle_errors=True)
parent_parser.add_argument('id', type=int, location='json')
parent_parser.add_argument('email', type=str, required=True, location='json')
parent_parser.add_argument('password', type=str, required=True, location='json')
parent_parser.add_argument('first_name', type=str, required=True, location='json')
parent_parser.add_argument('last_name', type=str, required=True, location='json')
parent_parser.add_argument('child_name', type=str, location='json')

drill_parser = reqparse.RequestParser(bundle_errors=True)
drill_parser.add_argument('id', type=int, location='json')
drill_parser.add_argument('name', type=str, required=True, location='json')
drill_parser.add_argument('description', type=str, required=True, location='json')

practice_parser = reqparse.RequestParser(bundle_errors=True)
practice_parser.add_argument('id', type=int, location='json')
practice_parser.add_argument('player_id', type=int, required=True, location='json')
practice_parser.add_argument('drill_id', type=int, required=True, location='json')
practice_parser.add_argument('speed', type=float, required=True, location='json')

playlist_parser = reqparse.RequestParser(bundle_errors=True)
playlist_parser.add_argument('player_id', type=int, location='json')
playlist_parser.add_argument('drill_id', type=int, location='json')

team_parser = reqparse.RequestParser(bundle_errors=True)
team_parser.add_argument('id', type=int, location='json')
team_parser.add_argument('player_id', type=int, location='json')
team_parser.add_argument('coach_id', type=int, location='json')
team_parser.add_argument('division', type=str, location='json')
team_parser.add_argument('league', type=str, location='json')
team_parser.add_argument('name', type=str, location='json')

class PlayerResource(Resource):
    @oauth.require_oauth('email')
    @marshal_with(player_fields)
    def get(self, id):
        player = Player.query.filter_by(id=id).first()

        if not player:
            abort(404, "Player %d: not found." % id)

        return player

    @marshal_with(player_fields)
    def put(self, id):
        player = Player.query.filter_by(id=id).first()

        if not player:
            abort(404, "Player %s: not found." % id)

        args = player_parser.parse_args()

        if args['hockey_level'] is not None:
            player.hockey_level = args['hockey_level']

        if args['skill_level'] is not None:
            player.skill_level = args['skill_level']

        if args['hand'] is not None:
            player.hand = args['hand']

        db.session.commit()

        return player

    def delete(self, id):
        player = Player.query.filter_by(id=id).first()

        if not player:
            abort(404, "Player %s: not found." % id)

        db.session.delete(player)
        db.session.commit()

        return {}, 204

class PlayerListResource(Resource):
    @marshal_with(player_fields)
    def get(self):
        return Player.query.all()

    @marshal_with(player_fields)
    def post(self):
        # Get arguments from request
        args = player_parser.parse_args()

        if 'id' not in args:
            highest = Player.query.order_by(Player.id).last()
            player_id = highest + 1
        else:
            player_id = args['id']

        player = Player(id=player_id, email=args['email'],
            first_name=args['first_name'], last_name=args['last_name'], hockey_level=args['hockey_level'],
            skill_level=args['skill_level'], hand=args['hand'])

        player.hash_password(args['password'])

        db.session.add(player)

        playlist = Playlist(id=player_id)
        db.session.add(playlist)

        player.playlist = playlist

        db.session.commit()

        return player, 201

class PlayerEmailsResource(Resource):
    @marshal_with(player_email_fields)
    def get(self):
        return Player.query.all()

class CoachResource(Resource):
    @marshal_with(coach_fields)
    def get(self, id):
        coach = Coach.query.filter_by(id=id).first()

        if not coach:
            abort(404, "Coach %s: not found." % id)

        return coach

    def delete(self, id):
        coach = Coach.query.filter_by(id=id).first()

        if not coach:
            abort(404, "Coach %s: not found." % id)

        db.session.delete(coach)
        db.session.commit()

        return {}, 204

class CoachListResource(Resource):
    @marshal_with(coach_fields)
    def get(self):
        return Coach.query.all()

    @marshal_with(coach_fields)
    def post(self):
        args = coach_parser.parse_args()

        if 'id' not in args:
            highest = Coach.query.order_by(Coach.id).last()
            coach_id = highest + 1
        else:
            coach_id = args['id']

        coach = Coach(id=coach_id, email=args['email'], password=args['password'],
            first_name=args['first_name'], last_name=args['last_name'])

        db.session.add(coach)
        db.session.commit()

        return coach, 201

class ParentResource(Resource):
    @marshal_with(parent_fields)
    def get(self, id):
        parent = Parent.query.filter_by(id=id).first()

        if not parent:
            abort(404, "Parent %s: not found." % id)

        return parent

    def delete(self, id):
        parent = Parent.query.filter_by(id=id).first()

        if not parent:
            abort(404, "Parent %s: not found." % id)

        db.session.delete(parent)
        db.session.commit()

        return {}, 204

class ParentListResource(Resource):
    @marshal_with(parent_fields)
    def get(self):
        return Parent.query.all()

    @marshal_with(parent_fields)
    def post(self):
        args = parent_parser.parse_args()

        if 'id' not in args:
            highest = Parent.query.order_by(Parent.id).last()
            parent_id = highest + 1
        else:
            parent_id = args['id']

        parent = Parent(id=parent_id, email=args['email'], password=args['password'],
            first_name=args['first_name'], last_name=args['last_name'])

        # TODO: Search for child's name

        db.session.add(parent)
        db.session.commit()

        return parent, 201

class DrillResource(Resource):
    @marshal_with(drill_fields)
    def get(self, id):
        drill = Drill.query.filter_by(id=id).first()

        if not drill:
            abort(404, "Drill %s: not found." % id)

        return drill

class DrillListResource(Resource):
    @marshal_with(drill_fields)
    def get(self):
        return Drill.query.all()

# TODO: Needs testing and refinement
class CatalogResource(Resource):
    @marshal_with(drill_fields)
    def get(self,id):
        player = Player.query.filter_by(id=id).first()
        print(player.id)
        playlist = player.playlist.drills.all()
        # FIXME: This is unfinished --> need to add drills not currently in playlist to catalog view

        drills = Drill.query.all()

        catalog = [drill for drill in drills if drill not in playlist]

        return catalog

class PracticeResource(Resource):
    @marshal_with(practice_fields)
    def get(self, id):
        practice = Practice.query.filter_by(id=id).first()

        if not practice:
            abort(404, "Practice %s: not found." % id)

        return practice

    def delete(self, id):
        practice = Practice.query.filter_by(id=id).first()

        if not practice:
            abort(404, "Practice %s: not found." % id)

        db.session.delete(practice)
        db.session.commit()

        return {}, 204

class PracticeListResource(Resource):
    @marshal_with(practice_fields)
    def get(self):
        return Practice.query.all()

    @marshal_with(practice_fields)
    def post(self):
        args = practice_parser.parse_args()

        if 'id' not in args:
            highest = Practice.query.order_by(Practice.id).last()
            practice_id = highest + 1
        else:
            practice_id = args['id']

        player = Player.query.filter_by(id=args['player_id']).first()
        if player is None:
            abort(404, "Player %s: not found." % args['player_id'])

        drill = Drill.query.filter_by(id=args['drill_id']).first()
        if drill is None:
            abort(404, "Drill %s: not found." % args['drill_id'])

        practice = Practice(id=practice_id, player_id=args['player_id'], drill_id=args['drill_id'],
            speed=args['speed'])

        db.session.add(practice)
        db.session.commit()

        return practice, 201

class PlaylistResource(Resource):
    @marshal_with(drill_fields)
    def get(self, id):
        playlist = Playlist.query.filter_by(id=id).first()
        if playlist is None:
            abort(404, "Playlist %s: not found." % id)

        return playlist.drills.all()

    @marshal_with(playlist_fields)
    def put(self, id):
        playlist = Playlist.query.filter_by(id=id).first()
        if playlist is None:
            abort(404, "Playlist %s: not found." % id)

        args = playlist_parser.parse_args()

        drill = Drill.query.filter_by(id=args['drill_id']).first()
        if drill is None:
            abort(404, "Drill %s: not found." % id)

        playlist.drills.append(drill)
        db.sessions.commit()

        return playlist

    def delete(self, id):
        playlist = Playlist.query.filter_by(id=id).first()

        if not playlist:
            abort(404, "Playlist %s: not found." % id)

        db.session.delete(playlist)
        db.session.commit()

        return {}, 204

class PlaylistListResource(Resource):
    @marshal_with(playlist_fields)
    def post(self):
        args = playlist_parser.parse_args()

        player = Player.query.filter_by(id=args['player_id']).first()
        if player is None:
            abort(404, "Player %s: not found." % args['player_id'])

        playlist = Playlist(id=player.id)

        db.session.add(playlist)

        player.playlist = playlist

        db.sesson.commit()

        return playlist, 201

class TeamResource(Resource):
    @marshal_with(team_fields)
    def get(self,id):
        team = Team.query.filter_by(id=id).first()

        if not team:
            abort(404, "Team %s: not found." % id)

        return team

    @marshal_with(team_fields)
    def put(self,id):
        team = Team.query.filter_by(id=id).first()

        if not team:
            abort(404, "Team %s: not found." % id)

        args = team_parser.parse_args()

        if args['player_id'] is not None:
            player = Player.query.filter_by(id=id).first()
            if not player:
                abort(404, "Player %s: not found." % id)
            team.players.append(player)

        if args['coach_id'] is not None:
            coach = Coach.query.filter_by(id=id).first()
            if not coach:
                abort(404, "Coach %s: not found." % id)
            team.coaches.append(coach)

        if args['division'] is not None:
            team.division = args['division']

        if args['league'] is not None:
            team.league = args['league']

        if args['name'] is not None:
            team.name = args['name']

        db.session.commit()

        return team

    def delete(self,id):
        team = Team.query.filter_by(id=id).first()

        if not team:
            abort(404, "Team %s: not found." % id)

        db.session.delete(team)

        return {}, 204


class TeamListResource(Resource):
    @marshal_with(team_fields)
    def get(self):
        return Team.query.all()

    @marshal_with(team_fields)
    def post(self):
        args = team_parser.parse_args()

        if 'id' not in args:
            highest = Team.query.order_by(Team.id).last()
            team_id = highest + 1
        else:
            team_id = args['id']

        team = Team(id=team_id, name=args['name'], division=args['division'],
            league=args['league'])

        if args['player_id'] is not None:
            player = Player.query.filter_by(id=args['player_id']).first()
            if player is None:
                abort(404, "Player %s: not found." % args['player_id'])
            team.players.append(player)

        coach = Coach.query.filter_by(id=id).first()
        if not coach:
            abort(404, "Coach %s: not found." % id)
        team.coaches.append(coach)

        db.session.add(team)
        db.session.commit()

        return team, 201
