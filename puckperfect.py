import os
import datetime
from datetime import timedelta
from flask import Flask, request, abort, url_for, redirect, session, render_template, flash, Response, jsonify, json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
from functools import wraps
from flask_restful import Resource, fields, reqparse, marshal_with, inputs, abort, Api
from flask_jwt import JWT, jwt_required, current_identity
from werkzeug.security import safe_str_cmp

from project_files.puckperfect.models import (
    db,
    Player,
    Coach,
    Parent,
    Drill,
    Practice,
    Playlist,
    Team
)

app = Flask(__name__)
app.static_folder = 'project_files/puckperfect/static'
app.template_folder = 'project_files/puckperfect/templates'
api = Api(app)

app.config.update(dict(
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='owner',
    PASSWORD='pass',
    JWT_EXPIRATION_DELTA = timedelta(days=7),

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(app.root_path, 'hockey.db')
))

db.init_app(app)

#--------------------------------------------------------------------------------------------

# Initialize database
@app.cli.command('initdb')
def initdb_command():
    """Creates the database tables."""
    db.drop_all()
    db.create_all()

    drill1 = Drill(id=1, name="Figure 8", description="Move ball in figure 8 around cones")
    drill2 = Drill(id=2, name="Three Cones", description="Stickhandle ball around triangle of cones")
    drill3 = Drill(id=3, name="Toe Drag", description="Pull ball back with toe of stick")
    drill4 = Drill(id=4, name="Side-to-Side Dribble", description="Stickhandle ball in front of feet")
    drill5 = Drill(id=5, name="Forehand-to-Backhand", description="Stickhandle ball next to body")
    drill6 = Drill(id=6, name="Around the World", description="Stickhandle ball from one side of body to other side")
    drill7 = Drill(id=7, name="Line Drill", description="Stickhandle ball through four cones arranged in a straight line")
    drill8 = Drill(id=8, name="Lucky Clover", description="Stickhandle ball in clover shape around four cones")
    drill9 = Drill(id=9, name="Wide Dribble", description="Stickhandle ball in front of feet using wide motions")

    db.session.add(drill1)
    db.session.add(drill2)
    db.session.add(drill3)
    db.session.add(drill4)
    db.session.add(drill5)
    db.session.add(drill6)
    db.session.add(drill7)
    db.session.add(drill8)
    db.session.add(drill9)

    player = Player(id=1, email="k.pucci103@gmail.com", password="pass", first_name="Katie", last_name="Pucci", hockey_level=5, skill_level=3, hand=True)

    db.session.add(player)

    playlist = Playlist(id=player.id)
    player.playlist = playlist

    db.session.add(playlist)

    player.playlist.drills.append(drill1)
    player.playlist.drills.append(drill2)
    player.playlist.drills.append(drill3)
    player.playlist.drills.append(drill4)
    player.playlist.drills.append(drill5)
    player.playlist.drills.append(drill6)
    player.playlist.drills.append(drill7)
    player.playlist.drills.append(drill8)
    player.playlist.drills.append(drill9)

    db.session.commit()

    print('Initialized the database.')

#--------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------

## Authentication

def authenticate(username, password):
    player = Player.query.filter_by(email=username).first()
    print(username)
    print(password)
    if player and player.check_password(password):
        return player

def identity(payload):
    print(payload)
    user_id = payload['identity']
    print(user_id)
    return Player.query.filter_by(id=user_id).first()

jwt = JWT(app, authenticate, identity)

def login_required(function_to_protect):
    @wraps(function_to_protect)
    def wrapper(*args, **kwargs):
        user_id = session.get('logged_in')
        if user_id:
            user = Player.query.filter_by(id=user_id).first()
            if user:
                # Success!
                return function_to_protect(*args, **kwargs)
            else:
                flash("Please login again to renew your session")
                return redirect(url_for('login'))
        else:
            flash("Please log in")
            return redirect(url_for('login'))
    return wrapper

#--------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------

## Resources

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
    @marshal_with(player_fields)
    @jwt_required()
    def get(self, id):
        player = Player.query.filter_by(id=id).first()

        if not player or not player.id == current_identity.id:
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

        player = Player(id=player_id, email=args['email'], password=args['password'],
            first_name=args['first_name'], last_name=args['last_name'], hockey_level=args['hockey_level'],
            skill_level=args['skill_level'], hand=args['hand'])

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

#---------------------------------------------------------
# Resources:

api.add_resource(PlayerListResource, '/players')
api.add_resource(PlayerResource, '/players/<int:id>')
api.add_resource(CoachListResource, '/coaches')
api.add_resource(CoachResource, '/coaches/<int:id>')
api.add_resource(ParentListResource, '/parents')
api.add_resource(ParentResource, '/parents/<int:id>')
api.add_resource(DrillListResource, '/drills')
api.add_resource(DrillResource, '/drills/<int:id>')
api.add_resource(PracticeListResource, '/practices')
api.add_resource(PracticeResource, '/practices/<int:id>')
api.add_resource(PlaylistResource, '/playlists/<int:id>')
api.add_resource(PlaylistListResource, '/playlists')
api.add_resource(TeamResource, '/teams/<int:id>')
api.add_resource(TeamListResource, '/teams')
api.add_resource(CatalogResource, '/catalog/<int:id>')
api.add_resource(PlayerEmailsResource, '/players/emails')

#--------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------

# Login page:
@app.route("/", methods=['GET','POST'])
def login():
    # If method is GET, render the login page
    if request.method == "GET":
        return render_template("login.html")

    # If posting to login page, then user is trying to login
    elif request.method == "POST":
        # Query DB for player with the given email
        player = Player.query.filter(Player.email==request.form["email"]).scalar()
        # If DB returns a player object, then user is a player
        if player is not None:
            # If password is correct, open their profile
            if player.check_password(request.form["password"]):
                session['logged_in'] = player.id
                return redirect(url_for("player_profile", id=player.id))
            # If password is wrong, tell user and go back to login page
            flash('Incorrect email or password')
            return render_template("login.html")

        # If DB doesn't return a player, then try a coach
        coach = Coach.query.filter_by(email=request.form["email"]).first()
        if coach is not None:
            if coach.check_password(request.form["password"]):
                session['logged_in'] = coach.id
                return redirect(url_for("coach_profile", id=coach.id))
            flash('Incorrect email or password')
            return render_template("login.html")

        # If DB doesn't return a coach, then try a parent
        parent = Parent.query.filter_by(email=request.form["email"]).first()
        if parent is not None:
            if parent.check_password(request.form["password"]):
                session['logged_in'] = parent.id
                return redirect(url_for("parent_profile", id=parent.id))
            flash('Incorrect email or password')
            return render_template("login.html")

        # If DB doesn't return a parent, then email isn't registered
        flash('Incorrect email or password')
        return render_template("login.html")

    return render_template("login.html")

#--------------------------------------------------------------------------------------------

# Logout
@app.route("/logout/")
def logout():
	session.pop("logged_in", None)
	flash("You've been signed out.")
	return redirect(url_for('default'))

#--------------------------------------------------------------------------------------------

# Registration page:
@app.route("/register/", methods=['GET','POST'])
def register():
    return render_template("register.html")

#--------------------------------------------------------------------------------------------

@app.route("/profile/", methods=['GET'])
@jwt_required()
def open_profile():
    print("open_profile")
    print(current_identity.id)
    player = Player.query.filter_by(id=current_identity.id).first()
    print(player)
    if player is not None:
        print("account type is player")
        session['logged_in'] = current_identity.id
        return redirect(url_for("player_profile", id=player.id))

    coach = Coach.query.filter_by(id=current_identity.id).first()
    if coach is not None:
        session['logged_in'] = current_identity.id
        return redirect(url_for("coach_profile", id=coach.id))

    parent = Parent.query.filter_by(id=current_identity.id).first()
    if parent is not None:
        session['logged_in'] = current_identity.id
        return redirect(url_for("parent_profile", id=parent.id))

    return redirect(url_for('default'))
#--------------------------------------------------------------------------------------------

# Player profile page:
# If viewing the profile without authorization, will display a limited view
# of the page. This is done in the javascript file when accessing the player's
# information.
@app.route("/player/<id>", methods=['GET'])
@login_required
def player_profile(id=None):
    return render_template("player_profile.html", id=id)

#--------------------------------------------------------------------------------------------

# Coach profile page:
@app.route("/coach/<id>", methods=['GET'])
@login_required
def coach_profile(id=None):
    return render_template("coach_profile.html")

#--------------------------------------------------------------------------------------------

# Parent profile page:
@app.route("/parent/<id>", methods=['GET'])
@login_required
def parent_profile(id=None):
    return render_template("parent_profile.html")

#--------------------------------------------------------------------------------------------

# Drill catalog page:
@app.route("/catalog/", methods=['GET'])
def catalog(id=None):
    # Get player
    # Get player's playlist
    # Get all drills
    # Filter out drills that are already in the playlist
    return render_template("catalog.html")


#--------------------------------------------------------------------------------------------

# Drill page:
@app.route("/drill/<id>", methods=['GET'])
def drill(id=None):
    return render_template("drill.html")

#--------------------------------------------------------------------------------------------

# Practice page:
@app.route("/practice/<id>", methods=['GET'])
def practice(id=None):
    return render_template("practice.html")

#--------------------------------------------------------------------------------------------

# Practice plan page:
@app.route("/practice_plan/", methods=['GET'])
def practice_plan(id=None):
    return render_template("practice_plan.html")

if __name__ == '__main__':
    app.run()
