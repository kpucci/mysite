import os, codecs
from sqlalchemy import exc
from flask import (
    Flask,
    request,
    abort,
    url_for,
    redirect,
    session,
    render_template,
    flash
)
from flask_restful import (
    reqparse,
    abort,
    Api,
    Resource
)
from models import (
    db,
    Project,
    Category
)
from resources import (
    ProjectResource,
    ProjectListResource,
    CategoryResource,
    CategoryListResource
)

app = Flask(__name__)
app.static_folder = 'static'
app.templates_folder = 'templates'
api = Api(app)

app.config.update(dict(
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='owner',
    PASSWORD='pass',

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(app.root_path, 'mysite.db')
))

db.init_app(app)

#---------------------------------------------------------
# Resources:

api.add_resource(ProjectListResource, '/projects')
api.add_resource(ProjectResource, '/projects/<int:project_id>')
api.add_resource(CategoryListResource, '/cats')
api.add_resource(CategoryResource, '/cats/<string:cat_name>')
#--------------------------------------------------------------------------------------------

@app.cli.command('initdb')
def initdb_command():
    db.drop_all()
    db.create_all()

    cat1 = Category(name='all')
    db.session.add(cat1)

    cat2 = Category(name='uncategorized')
    db.session.add(cat2)

    cat3 = Category(name='web')
    db.session.add(cat3)

    cat4 = Category(name='embedded')
    db.session.add(cat4)

    cat5 = Category(name='art')
    db.session.add(cat5)

    proj1 = Project(
        name='chat',
        img='chat.png',
        text="Chatty Kathy",
        tagline="Python | Flask | SQLAlchemy | JavaScript | HTML | CSS | AJAX",
        next="catering",
        previous=""
    )
    db.session.add(proj1)

    proj1.categories.append(cat1)
    proj1.categories.append(cat3)
    cat1.projects.append(proj1)
    cat3.projects.append(proj1)

    proj2 = Project(
        name='catering',
        img='catering.png',
        text="So You Think You Can Cater",
        tagline="Python | Flask | SQLAlchemy | JavaScript | HTML | CSS",
        next="budget",
        previous="chat"
    )
    db.session.add(proj2)

    proj2.categories.append(cat1)
    proj2.categories.append(cat3)
    cat1.projects.append(proj2)
    cat3.projects.append(proj2)

    proj3 = Project(
        name='budget',
        img='budget.png',
        text="Money on My Mind",
        tagline="Python | Flask | SQLAlchemy | JavaScript | HTML | CSS | AJAX | REST",
        next="battleship",
        previous='catering'
    )
    db.session.add(proj3)

    proj3.categories.append(cat1)
    proj3.categories.append(cat3)
    cat1.projects.append(proj3)
    cat3.projects.append(proj3)

    proj4 = Project(
        name='battleship',
        img='battleship.png',
        text="You Sunk My Battleship",
        tagline="JavaScript | HTML | CSS",
        next="",
        previous="budget"
    )
    db.session.add(proj4)

    proj4.categories.append(cat1)
    proj4.categories.append(cat3)
    cat1.projects.append(proj4)
    cat3.projects.append(proj4)

    db.session.commit()

    print('Initialized the database.')

#--------------------------------------------------------------------------------------------
# Skills

skills = [
	{'Name':'Java', 'Level':'Advanced'},
	{'Name':'Python', 'Level':'Proficient'},
	{'Name':'JavaScript', 'Level':'Proficient'},
	{'Name':'HTML5', 'Level':'Proficient'},
	{'Name':'MAPDL', 'Level':'Proficient'},
	{'Name':'SolidWorks', 'Level':'Expert'},
	{'Name':'ANSYS', 'Level':'Advanced'},
	{'Name':'AutoCAD', 'Level':'Proficient'}
]

#--------------------------------------------------------------------------------------------

# Home page:
@app.route("/")
def default():
    return render_template("home.html", skills=skills)

#--------------------------------------------------------------------------------------------

# Project page:
@app.route("/project/<projectname>")
def project_page(projectname=None):
    project = Project.query.filter_by(name=projectname.lower()).first()
    nextURL = None
    prevURL = None
    if project.next:
        nextURL = url_for('project_page', projectname=project.next)
    if project.previous:
        prevURL = url_for('project_page', projectname=project.previous)
    return render_template(project.name + "_project.html", projectname=project.text, tagline=project.tagline, image=url_for('static', filename=projectname+'_project.jpg'), next=nextURL, previous=prevURL, launch='/'+project.name)
