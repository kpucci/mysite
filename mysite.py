import os
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

    proj1 = Project(name='Chat', img='chat.png')
    db.session.add(proj1)

    proj1.categories.append(cat1)
    proj1.categories.append(cat3)
    cat1.projects.append(proj1)
    cat3.projects.append(proj1)

    proj2 = Project(name='Catering', img='catering.png')
    db.session.add(proj2)

    proj2.categories.append(cat1)
    proj2.categories.append(cat3)
    cat1.projects.append(proj2)
    cat3.projects.append(proj2)

    proj3 = Project(name='Budget', img='budget.png')
    db.session.add(proj3)

    proj3.categories.append(cat1)
    proj3.categories.append(cat3)
    cat1.projects.append(proj3)
    cat3.projects.append(proj3)

    proj4 = Project(name='Battleship', img='battleship.png')
    db.session.add(proj4)

    proj4.categories.append(cat1)
    proj4.categories.append(cat3)
    cat1.projects.append(proj4)
    cat3.projects.append(proj4)

    db.session.commit()

    print('Initialized the database.')

# Home page:
# GET - Visit home page
# POST - Signin --> Redirect to profile page if successful
@app.route("/")
def default():
    return render_template("home.html")

#--------------------------------------------------------------------------------------------
