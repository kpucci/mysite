from flask_restful import Resource, fields, reqparse, marshal_with, abort
from flask import request
from models import db, Project, Category

project_fields = {
	'name': fields.String,
    'img': fields.String
}

category_fields = {
	'name': fields.String
}

project_parser = reqparse.RequestParser(bundle_errors=True)
project_parser.add_argument('name', type=str, required=True, location='json')
project_parser.add_argument('img', type=str, required=True, location='json')
# project_parser.add_argument('category', type=str, location='json')

cat_parser = reqparse.RequestParser(bundle_errors=True)
cat_parser.add_argument('name', type=str, required=True, location='json')
project_parser.add_argument('img', type=str, required=True, location='json')
project_parser.add_argument('category', type=str, location='json')

class ProjectResource(Resource):
    @marshal_with(project_fields)
    def get(self, project_id):
        return projects[project_id]

class ProjectListResource(Resource):
    @marshal_with(project_fields)
    def get(self):
        return projects

    @marshal_with(project_fields)
    def post(self):
        # Get arguments from request
        args = project_parser.parse_args()

        # Get next purchase id
        project_id = len(projects)+1

        # If the request contains a category
        if 'category' in args:
            cat = args['category']
        else:
            cat = 'uncategorized'

        project = {
            'name': args['name'],
            'category': cat,
            'img': args['img']
        }

        # If the category exists in categories list, add project to category
        if cat in categories:
            category = categories[cat]
            cat_projects = category['projects']
            cat_projects.append(project)

            all_cat = categories['all']
            all_cat['projects'].append(project)

        # Otherwise, abort and warn user that the category doesn't exist
        else:
            abort(404, message="Category {} doesn't exist".format(args['category']))


        # Add purchase to purchase list and return it
        projects[project_id] = project
        return projects[project_id], 201

class CategoryResource(Resource):
    @marshal_with(project_fields)
    def get(self, cat_name):
        category = Category.query.filter_by(name=cat_name).first()

        if not category:
            abort(404, "Category %s: not found." % cat_name)

        return category.projects.all()

    @marshal_with(category_fields)
    def delete(self, cat_name):
        # Can't delete uncategorized category
        if cat_name.lower() == "uncategorized":
            abort(403, message="Cannot delete the 'uncategorized' category")
        # Can't delete uncategorized category
        elif cat_name.lower() == "all":
            abort(403, message="Cannot delete the 'all' category")
        # If the category exists
        elif cat_name in categories:
            # Get uncategorized purchase list
            uncat = categories['uncategorized']
            uncat_project = uncat['projects']
            # For each purchase in purchase list
            for project in projects:
                # If the purchase's category is the one being deleted
                if projects[project]["category"] == cat_name:
                    # Set purchase category to uncategorized
                    projects[project]["category"] = "uncategorized";
                    uncat_project.append(projects[project])
            # Delete category from list
            del categories[cat_name]
            return '', 204
        # Otherwise, return
        return '', 204

class CategoryListResource(Resource):
    @marshal_with(category_fields)
    def get(self):
        # Return a list comprehension of category list --> Easier for processing in js
        return [categories[index] for index in categories]

    @marshal_with(category_fields)
    def post(self):
        args = cat_parser.parse_args()
        if args['name'].lower() == 'uncategorized':
            abort(403, message="Cannot add a category with name 'uncategorized'")
        elif args['name'].lower() == 'all':
            abort(403, message="Cannot add a category with name 'all'")

        category = {
            'name': args['name'],
            'projects': []
        }

        categories[category['name']] = category

        # Return a list comprehension of category list --> Easier for processing in js
        return [categories[index] for index in categories], 201
