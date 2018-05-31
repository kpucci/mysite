import os
import datetime
import re
from flask import Flask, request, abort, url_for, redirect, session, render_template, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc

from models import db, Customer, Staff, Event

app = Flask(__name__)
app.static_folder = 'static'

app.config.update(dict(
	DEBUG=True,
	SECRET_KEY='development key',
	USERNAME='owner',
	PASSWORD='pass',

	SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(app.root_path, 'catering.db')
))

db.init_app(app)

#--------------------------------------------------------------------------------------------

# Initialize database to have owner as a staff member with admin privileges
@app.cli.command('initdb')
def initdb_command():
	"""Creates the database tables."""
	db.drop_all()
	db.create_all()
	owner = Staff(firstname="Katie", lastname="Pucci", username="owner", password="pass", email="katie@kkatering.com", admin=True)
	db.session.add(owner)
	db.session.commit()
	print('Initialized the database.')

#--------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------

# Initialize database to have owner as a staff member with admin privileges
@app.cli.command('testdb')
def testdb_command():
	"""Creates the database tables."""
	db.drop_all()
	db.create_all()

	# Add owner
	owner = Staff(firstname="Katie", lastname="Pucci", username="owner", password="pass", email="katie@kkatering.com", admin=True)
	db.session.add(owner)
	print("Added owner")

	# Create a customer
	customer_1 = Customer(username="Customer1", password="password1", email="Customer@me.com")
	print("Created customer")
	db.session.add(customer_1)
	print("Added customer")

	start_1 = datetime.date(2017,10,5)
	end_1 = datetime.date(2017,10,6)

	# Create an event
	event_1 = Event(name="Event 1", start=start_1, end=end_1)
	print("Created event")

	# Append the event to customer and add event
	customer_1.events.append(event_1)
	print("Appended event to customer")
	db.session.add(event_1)
	print("Added event")

	# Set event customer id
	event_1.customer = customer_1
	print("Set event customer id")
	print("Customer name: " + event_1.customer.username)

	# Create a staff member
	staff_1 = Staff(firstname="Jane",
			lastname="Doe", username="janedoe1",
			password="janedoe1",
			email="jane.doe@me.com",
			admin=False
		)
	print("Created staff member 1")
	db.session.add(staff_1)
	print("Added staff member 1")

	# Create another staff member
	staff_2 = Staff(firstname="John",
			lastname="Deer", username="johndeer1",
			password="johndeer1",
			email="john.deer@me.com",
			admin=False
		)
	print("Created staff member 2")
	db.session.add(staff_2)
	print("Added staff member 2")

	# Append event to staff_1's schedule
	staff_1.schedule.append(event_1)

	# Append staff member to event
	# event_1.workers.append(staff_1)

	# Append event to staff_1's schedule
	staff_2.schedule.append(event_1)

	# Append staff member to event
	# event_1.workers.append(staff_2)

	start_2 = datetime.date(2017,11,5)
	end_2 = datetime.date(2017,11,6)

	# Create another event
	event_2 = Event(name="Event 2", start=start_2, end=end_2)
	print("Created event 2")

	# Append the event to customer and add event
	customer_1.events.append(event_2)
	print("Appended event 2 to customer")
	db.session.add(event_2)
	print("Added event 2")

	# Set event customer id
	event_2.customer = customer_1
	print("Set event customer id")

	# Append event to staff_1's schedule
	# staff_1.schedule.append(event_2)

	# Append staff member to event
	# event_2.workers.append(staff_1)

	db.session.commit()
	print('Initialized the database.')

	staff1 = Staff.query.filter_by(username="janedoe1").first()
	staff1_events = staff_1.schedule
	for e in staff1_events:
		print("Event:  ", e.name)

	event1 = Event.query.filter_by(name="Event 1").first()
	event1_staff = event1.workers
	for w in event1_staff:
		print("Staff: ", w.username)


#--------------------------------------------------------------------------------------------

# Home page:
# GET - Visit home page
# POST - Signin --> Redirect to profile page if successful
@app.route("/", methods=['GET','POST'])
def default():
	if request.method == "GET":
		if "logged_in" in session:
			return render_template("home.html", loggedIn=True)
		else:
			return render_template("home.html", loggedIn=False)
	elif request.method == "POST":
		customerUser = Customer.query.filter(Customer.username.like(request.form["username"]), Customer.password.like(request.form["password"])).scalar()
		staffUser = Staff.query.filter(Staff.username.like(request.form["username"]), Staff.password.like(request.form["password"])).scalar()

		if customerUser is not None:
			session['logged_in'] = request.form["username"]
			return redirect(url_for("customer_profile", username=session.get("logged_in")))
		elif staffUser is not None:
			session['logged_in'] = request.form["username"]
			return redirect(url_for("profile"))
		else:
			flash('Incorrect username or password')
			return render_template("home.html", loggedIn=False)
	else:
		return render_template("home.html", loggedIn=False)

#--------------------------------------------------------------------------------------------

# New Customer:
# GET - Visit new customer page
# POST - Create new user in db, log them in, and redirect to profile page
@app.route("/new_customer/", methods=['GET','POST'])
def new_customer():
	if request.method == "GET":
		if "logged_in" in session:
			return render_template("new_customer.html", loggedIn=True)
		else:
			return render_template("new_customer.html", loggedIn=False)
	elif request.method == "POST":
		if request.form["password"] != request.form["password2"]:
			flash("The passwords did not match.")
			return redirect(url_for('new_customer'))
		elif not re.match(r"[^@]+@[^@]+\.[^@]+", request.form["email"]):
			flash("Please enter a valid email address.")
			return redirect(url_for('new_customer'))
		elif Customer.query.filter_by(username=request.form["username"]).scalar() is not None:
			flash("That username has been taken already.")
			return redirect(url_for('new_customer'))
		elif Customer.query.filter_by(email=request.form["email"]).scalar() is not None:
			flash("There's already a user with that email.")
			return redirect(url_for('new_customer'))
		newUser = Customer(username=request.form["username"], password=request.form["password"], email=request.form["email"])
		db.session.add(newUser)
		try:
			db.session.commit()
			session['logged_in'] = request.form["username"]
			return redirect(url_for('customer_profile', username=request.form["username"]))
		except exc.SQLAlchemyError:
			flash("There was a problem creating your account.")
			return redirect(url_for('default'))

#--------------------------------------------------------------------------------------------

@app.route("/new_staff/", methods=["GET", "POST"])
def new_staff():
	if request.method == "GET":
		if Staff.query.filter(Staff.username.like(session.get("logged_in")), Staff.admin.like(1)).scalar() is None:
			flash("You do not have permission to access that page.")
			return redirect(url_for("default"))
		return render_template("new_staff.html")
	elif request.method == "POST":
		if not re.match(r"[^@]+@[^@]+\.[^@]+", request.form["email"]):
			flash("Please enter a valid email address.")
			return redirect(url_for('new_staff'))
		elif Staff.query.filter_by(username=request.form["username"]).scalar() is not None:
			flash("There's already a staff member with that username.")
			return redirect(url_for('new_staff'))
		elif Staff.query.filter_by(email=request.form["email"]).scalar() is not None:
			flash("There's already a staff member with that email.")
			return redirect(url_for('new_staff'))
		newStaff = Staff(firstname=request.form["firstname"],
			lastname=request.form["lastname"], username=request.form["username"],
			password=request.form["password"],
			email=request.form["email"],
			admin=False
		)
		db.session.add(newStaff)
		try:
			db.session.commit()
			flash("{}'s profile was successfully created.".format(request.form["firstname"]))
			return redirect(url_for('new_staff'))
		except exc.SQLAlchemyError:
			flash("There was a problem adding the staff member.")
			return redirect(url_for('new_staff'))


#--------------------------------------------------------------------------------------------


# Profile:
# GET - Redirect to customer, staff, or admin profile subtype
# NEED THIS FOR ACCOUNT BUTTON
@app.route("/profile/")
def profile():
	# if request.method == "GET":
	# print(type(Staff.query.filter_by(username=session.get("logged_in")).scalar()))
	# print(type(Customer.query.filter_by(username=session.get("logged_in")).scalar()))
	# print(type(Staff.query.filter(Staff.username.like(session.get("logged_in")), Staff.admin.like(1)).scalar()))
	if "logged_in" in session:
		print("logged_in: " + session.get("logged_in"))
		if Customer.query.filter_by(username=session.get("logged_in")).scalar() is not None:
			print("Load customer profile")
			return redirect(url_for("customer_profile", username=session.get("logged_in")))
		elif Staff.query.filter_by(username=session.get("logged_in")).scalar() is not None:
			if Staff.query.filter(Staff.username.like(session.get("logged_in")), Staff.admin.like(1)).scalar() is not None:
				print("Load owner profile")
				return redirect(url_for('admin_profile', username=session.get("logged_in")))
			else:
				print("Load staff profile")
				return redirect(url_for('staff_profile', username=session.get("logged_in")))
		else:
			flash("This account doesn't exist.")
			return redirect(url_for('default'))
	else:
		flash('You need to login to access this account')
		return redirect(url_for('default'))

	flash('There was a problem trying to access your account.')
	return redirect(url_for('default'))

#--------------------------------------------------------------------------------------------

# Customer Profile:
# GET - Go to profile
# POST - Request event
@app.route("/customer/<username>", methods=["GET", "POST"])
def customer_profile(username=None):
	if request.method == "GET":
		if Customer.query.filter_by(username=session.get("logged_in")).scalar() is not None:
			customerObj = Customer.query.filter_by(username=session.get("logged_in")).first()
			events_list = Event.query.order_by(Event.start).filter((Event.customer==customerObj) & (Event.end>=datetime.datetime.now())).all()
			return render_template("customer.html", username=session.get("logged_in"), datemin=datetime.datetime.now().strftime('%Y-%m-%d'), events=events_list)
		else:
			flash('You need to login to access this account')
			return redirect(url_for('default'))
	elif request.method == "POST":
		if "cancel_button" in request.form:
			customerObj = Customer.query.filter_by(username=session.get("logged_in")).scalar()
			event_to_delete = Event.query.filter((Event.name==request.form["cancel_button"]) & (Event.customer==customerObj)).delete()
			try:
				db.session.commit()
				flash("The event was canceled.")
				return redirect(url_for("customer_profile", username=session.get("logged_in")))
			except exc.SQLAlchemyError:
				flash("There was a problem canceling the event.")
				return redirect(url_for("customer_profile", username=session.get("logged_in")))
		else:
			if request.form["endDate"] < request.form["startDate"]:
				flash("The end date must be greater than or equal to the start date.")
				return redirect(url_for("customer_profile", username=session.get("logged_in")))
			elif Event.query.filter_by(name=request.form["eventName"]).scalar() is not None:
				flash("There is already an event with that name.")
				return redirect(url_for("customer_profile", username=session.get("logged_in")))
			elif Event.query.filter((Event.start==request.form["startDate"]) | (Event.end == request.form["endDate"]) | (Event.start==request.form["endDate"]) | (Event.end==request.form["startDate"])).scalar() is not None:
				flash("There is already an event scheduled for the requested dates.")
				return redirect(url_for("customer_profile", username=session.get("logged_in")))
			elif Event.query.filter((Event.start<=request.form["endDate"]) & (Event.end >= request.form["endDate"])).scalar() is not None:
				flash("There is already an event scheduled for the requested dates.")
				return redirect(url_for("customer_profile", username=session.get("logged_in")))
			elif Event.query.filter((Event.start<=request.form["startDate"]) & (Event.end>=request.form["startDate"])).scalar() is not None:
				flash("There is already an event scheduled for the requested dates.")
				return redirect(url_for("customer_profile", username=session.get("logged_in")))
			elif Event.query.filter((Event.start>=request.form["startDate"]) & (Event.end<=request.form["endDate"])).scalar() is not None:
				flash("There is already an event scheduled for the requested dates.")
				return redirect(url_for("customer_profile", username=session.get("logged_in")))

			currCustomer = Customer.query.filter_by(username=session.get("logged_in")).first()
			s_split = request.form["startDate"].split("-")
			e_split = request.form["endDate"].split("-")
			start_date = datetime.date(int(s_split[0]),int(s_split[1]),int(s_split[2]))
			end_date = datetime.date(int(e_split[0]),int(e_split[1]),int(e_split[2]))
			# Add event for customer
			newEvent = Event(name=request.form["eventName"], start=start_date, end=end_date)

			currCustomer.events.append(newEvent)
			db.session.add(newEvent)
			newEvent.customer = currCustomer

			try:
				db.session.commit()
				flash("The event was successfully created.")
				return redirect(url_for("customer_profile", username=session.get("logged_in")))
			except exc.SQLAlchemyError:
				flash("There was a problem scheduling the event.")
				return redirect(url_for("customer_profile", username=session.get("logged_in")))


#--------------------------------------------------------------------------------------------

# Staff Profile:
# GET - Go to profile
# POST - Request to work an event
@app.route("/staff/<username>", methods=["GET", "POST"])
def staff_profile(username=None):
	if Staff.query.filter_by(username=session.get("logged_in")).scalar() is not None:
		staff_member = Staff.query.filter_by(username=session.get("logged_in")).first()
		if request.method == "GET":

			# Get list of events with less than 3 workers
			events_to_work = []
			events_working = []
			events_all = Event.query.order_by(Event.start).filter(Event.end>=datetime.datetime.now()).all()
			for e in events_all:
				e_workers = e.workers.all()
				if len(e_workers) < 3 and staff_member not in e_workers and e.start >= datetime.datetime.now():
					events_to_work.append(e)
				elif staff_member in e_workers:
					events_working.append(e)
			return render_template("staff.html", username=session.get("logged_in"), work=events_working, events=events_to_work)

		else:
			event_name = request.form["event_button"]
			event = Event.query.filter_by(name=event_name).first()
			staff_member.schedule.append(event)
			try:
				db.session.commit()
				flash("The event was added to your schedule.")
				return redirect(url_for("staff_profile", username=session.get("logged_in")))
			except exc.SQLAlchemyError:
				flash("There was a problem adding the event to your schedule.")
				return redirect(url_for("staff_profile", username=session.get("logged_in")))
	flash('You need to login to access this account')
	return redirect(url_for('default'))

#--------------------------------------------------------------------------------------------

# Admin Profile:
# GET - Go to profile
@app.route("/admin/<username>")
def admin_profile(username="owner"):
	if Staff.query.filter(Staff.username.like(session.get("logged_in")), Staff.admin.like(1)).scalar() is not None:
		owner = Staff.query.filter(Staff.username.like(session.get("logged_in")), Staff.admin.like(1)).first()
		events_all = Event.query.order_by(Event.start).filter(Event.end>=datetime.datetime.now()).all()
		no_staff_events = list()
		event_staff = list()
		for e in events_all:
			e_workers = e.workers.all()
			event_staff.append(e_workers)
			if len(e_workers) == 0:
				no_staff_events.append(e)
		return render_template("admin.html", username=username, events=events_all, no_staff=no_staff_events)
	else:
		flash("You don't have permission to access that page")
		return redirect(url_for("default"))

#--------------------------------------------------------------------------------------------

@app.route("/logout/")
def logout():
	session.pop("logged_in", None)
	flash("You've been signed out.")
	return redirect(url_for('default'))

if __name__ == "__main__":
	app.run()
