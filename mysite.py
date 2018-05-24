import os
import datetime
import re
from flask import Flask, request, abort, url_for, redirect, session, render_template, flash

app = Flask(__name__)
app.static_folder = 'static'
api = Api(app)

app.config.update(dict(
    DEBUG=True,
    SECRET_KEY='development key'
))

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
