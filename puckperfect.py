import os
import datetime
import re
from flask import Flask, request, abort, url_for, redirect, session, render_template, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc

from project_files.puckperfect.resources import (
    PlayerResource,
    PlayerListResource,
    CoachResource,
    CoachListResource,
    ParentResource,
    ParentListResource,
    DrillResource,
    DrillListResource,
    PracticeResource,
    PracticeListResource,
    PlaylistResource,
    PlaylistListResource,
    PlayerEmailsResource,
    TeamResource,
    TeamListResource,
    CatalogResource
)
from flask_restful import (
    reqparse,
    abort,
    Api,
    Resource
)

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

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(app.root_path, 'hockey.db')
))

db.init_app(app)

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

# Login page:
@app.route("/", methods=['GET','POST'])
def login():
    # TODO: Add authentication
    # TODO: Remember me functionality

    if request.method == "GET":
        if "logged_in" in session:
            return render_template("login.html", loggedIn=True)
        else:
            return render_template("login.html", loggedIn=False)
    elif request.method == "POST":
        player = Player.query.filter(Player.email.like(request.form["email"]), Player.password.like(request.form["password"])).scalar()
        coach = Coach.query.filter(Coach.email.like(request.form["email"]), Coach.password.like(request.form["password"])).scalar()
        parent = Parent.query.filter(Parent.email.like(request.form["email"]), Parent.password.like(request.form["password"])).scalar()

        if player is not None:
            session['logged_in'] = request.form["email"]
            return redirect(url_for("player_profile", id=player.id))
        elif coach is not None:
            session['logged_in'] = request.form["email"]
            return redirect(url_for("coach_profile", id=coach.id))
        elif parent is not None:
            session['logged_in'] = request.form["email"]
            return redirect(url_for("parent_profile", id=parent.id))
        else:
            flash('Incorrect email or password')
            return render_template("login.html", loggedIn=False)
    else:
        return render_template("login.html", loggedIn=False)

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

# Player profile page:
@app.route("/player/<id>", methods=['GET'])
def player_profile(id=None):
    return render_template("player_profile.html", id=id)

#--------------------------------------------------------------------------------------------

# Coach profile page:
@app.route("/coach/<id>", methods=['GET'])
def coach_profile(id=None):
    return render_template("coach_profile.html")

#--------------------------------------------------------------------------------------------

# Parent profile page:
@app.route("/parent/<id>", methods=['GET'])
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


if __name__ == "__main__":
	app.run()
