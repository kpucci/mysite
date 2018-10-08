from flask_sqlalchemy import SQLAlchemy

# Instantiate a database object
puckperfect_db = SQLAlchemy()

# Player has many teams
# Team has many players --> Many-to-many
teams1 = db.Table('teams1',
    db.Column('player_id', db.Integer, db.ForeignKey('player.id')),
    db.Column('team_id', db.Integer, db.ForeignKey('team.id'))
)

players = db.Table('players',
    db.Column('team_id', db.Integer, db.ForeignKey('team.id')),
    db.Column('player_id', db.Integer, db.ForeignKey('player.id'))
)

# Coach has many teams
# Team has many coaches --> Many-to-many
coaches = db.Table('coaches',
    db.Column('team_id', db.Integer, db.ForeignKey('team.id')),
    db.Column('coach_id', db.Integer, db.ForeignKey('coach.id'))
)

teams2 = db.Table('teams2',
    db.Column('coach_id', db.Integer, db.ForeignKey('coach.id')),
    db.Column('team_id', db.Integer, db.ForeignKey('team.id'))
)

# Playlist has many drills
# Drill has many playlists --> Many-to-many
drills = db.Table('drills',
    db.Column('playlist_id', db.Integer, db.ForeignKey('playlist.id')),
    db.Column('drill_id', db.Integer, db.ForeignKey('drill.id'))
)

playlists = db.Table('playlists',
    db.Column('drill_id', db.Integer, db.ForeignKey('drill.id')),
    db.Column('playlist_id', db.Integer, db.ForeignKey('playlist.id'))
)


class Player(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    email = db.Column(db.String(80), unique = True)
    password = db.Column(db.String(100))

    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))

    hockey_level = db.Column(db.Integer)
    skill_level = db.Column(db.Integer)
    age = db.Column(db.Integer)
    hand = db.Column(db.Boolean)

    # Playlist has one player
    # Player has one playlist --> One-to-one
    playlist_id = db.Column(db.Integer, db.ForeignKey('playlist.id'))
    playlist = db.relationship("Playlist", backref=db.backref("player", uselist=False))

    # Many-to-many
    teams1 = db.relationship('Team', secondary='teams1',lazy='dynamic', backref='player')

    # Practice has one drill
    # Drill has many practices --> Many-to-one
    parent_id = db.Column(db.Integer, db.ForeignKey('parent.id'))
    parent = db.relationship("Parent", backref="players")

    # NOTE: Backref to practices

    def _repr_(self):
        return "<Player {}>".format(repr(self.id))

class Coach(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    email = db.Column(db.String(80), unique = True)
    password = db.Column(db.String(100))

    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))

    # Many-to-many
    teams2 = db.relationship('Team', secondary='teams2',lazy='dynamic', backref='coach')

    def _repr_(self):
        return "<Coach {}>".format(repr(self.id))

class Parent(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    email = db.Column(db.String(80), unique = True)
    password = db.Column(db.String(100))

    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))

    # NOTE: Backref to players

    def _repr_(self):
        return "<Parent {}>".format(repr(self.id))

class Drill(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    name = db.Column(db.String(80))
    description = db.Column(db.String(200))
    image = db.Column(db.String(100))

    # Many-to-many
    playlists = db.relationship('Playlist', secondary='playlists',lazy='dynamic', backref='drill')

    def _repr_(self):
        return "<Drill {}>".format(repr(self.id))

class Playlist(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    # NOTE: Backref to player

    # Many-to-many
    drills = db.relationship('Drill', secondary='drills',lazy='dynamic',backref='playlist')

    def _repr_(self):
        return "<Playlist {}>".format(repr(self.id))

class Practice(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)

    # Practice has one player
    # Player has many practices --> Many-to-one
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'))
    player = db.relationship("Player", backref="practices")

    # Practice has one drill
    # Drill has many practices --> Many-to-one
    drill_id = db.Column(db.Integer, db.ForeignKey('drill.id'))
    drill = db.relationship("Drill")

    speed = db.Column(db.Float)
    # TODO: Add other data

    def _repr_(self):
        return "<Practice {}>".format(repr(self.id))

class Team(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    name = db.Column(db.String(80))
    league = db.Column(db.String(80))
    division = db.Column(db.String(80))

    # Many-to-many
    coaches = db.relationship('Coach', secondary='coaches',lazy='dynamic',backref='team')

    # Many-to-many
    players = db.relationship('Player', secondary='players',lazy='dynamic',backref='team')

    def _repr_(self):
        return "<Team {}>".format(repr(self.id))