from flask_sqlalchemy import SQLAlchemy

# Instantiate a database object
db = SQLAlchemy()


schedule = db.Table('schedule',
	db.Column('event_id', db.Integer, db.ForeignKey('event.id')),
	db.Column('staff_id', db.Integer, db.ForeignKey('staff.id'))
)


class Customer(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	username = db.Column(db.String(80), unique = True)
	password = db.Column(db.String(100))
	email = db.Column(db.String(120), unique = True)
	events = db.relationship('Event', backref='customer', lazy=True)

	def _repr_(self):
		return "<Customer {}>".format(repr(self.username))

class Staff(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	firstname = db.Column(db.String(35))
	lastname = db.Column(db.String(50))
	username = db.Column(db.String(80), unique = True)
	password = db.Column(db.String(100))
	email = db.Column(db.String(120), unique = True)
	admin = db.Column(db.Boolean)
	schedule = db.relationship('Event', secondary=schedule, lazy='dynamic', backref=db.backref('workers',lazy='dynamic'))

	def _repr_(self):
		return "<Staff {}>".format(repr(self.username))


class Event(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(150), unique = True)
	customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
	start = db.Column(db.DateTime)
	end = db.Column(db.DateTime)

	def _repr_(self):
		return "<Event {}>".format(repr(self.name))
