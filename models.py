from flask_sqlalchemy import SQLAlchemy

# Instantiate a database object
db = SQLAlchemy()

# One project has many categories
# One category has many projects

# One user joins one room
# One room has many users

# One room has many messages
# One message has one room

projects = db.Table('projects',
    db.Column('category_name', db.String, db.ForeignKey('category.name')),
    db.Column('project_name', db.String, db.ForeignKey('project.name'))
)

categories = db.Table('categories',
    db.Column('project_name', db.String, db.ForeignKey('project.name')),
    db.Column('category_name', db.String, db.ForeignKey('category.name'))
)

class Project(db.Model):
    name = db.Column(db.String(80), unique = True, primary_key = True)
    img = db.Column(db.String(80), unique = True)

    categories = db.relationship('Category', secondary='categories',lazy='dynamic',backref='project')

    # curr_room_id = db.Column(db.String, db.ForeignKey('chat_room.name'))
    # curr_room = db.relationship('ChatRoom',secondary='users',backref='users', lazy='dynamic')

    def _repr_(self):
        return "<Project {}>".format(repr(self.name))

class Category(db.Model):
    name = db.Column(db.String(80), unique = True, primary_key = True)
    # creator_id = db.Column(db.String, db.ForeignKey('user.username'))
    # creator = db.relationship('User', backref='rooms', foreign_keys=[creator_id])
    projects = db.relationship('Project', secondary='projects',lazy='dynamic', backref='category')

    def _repr_(self):
        return "<Category {}>".format(repr(self.name))
