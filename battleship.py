import os
from flask import Flask, render_template, url_for

app = Flask(__name__)
app.static_folder = 'project_files/battleship/static'
app.template_folder = 'project_files/battleship/templates'

app.config.update(dict(
    DEBUG=True,
    SECRET_KEY='development key',
))

# Home page:
# GET - Visit home page
# POST - Signin --> Redirect to profile page if successful
@app.route("/")
def default():
    return render_template("battleship.html")

#--------------------------------------------------------------------------------------------
