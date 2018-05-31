import os
import re
import datetime
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
    Resource,
    fields,
    marshal_with
)
from flask import request

app = Flask(__name__)
app.static_folder = 'project_files/budget/static'
app.template_folder = 'project_files/budget/templates'
api = Api(app)

app.config.update(dict(
    DEBUG=True,
    SECRET_KEY='development key'
))


#---------------------------------------------------------
# Data setup:

purchases = {}
categories = {}

#---------------------------------------------------------
# Resources:

purchase_parser = reqparse.RequestParser(bundle_errors=True)
purchase_parser.add_argument('name', type=str, required=True, location='json')
purchase_parser.add_argument('amount', type=float, required=True, location='json')
purchase_parser.add_argument('category', type=str, location='json')
purchase_parser.add_argument('date', type=str, required=True, location='json')

cat_parser = reqparse.RequestParser(bundle_errors=True)
cat_parser.add_argument('name', type=str, required=True, location='json')
cat_parser.add_argument('budget', type=float, location='json')

cat_put_parser = reqparse.RequestParser(bundle_errors=True)
cat_put_parser.add_argument('budget', required=True, type=float, location='json')

class PurchaseResource(Resource):
    def get(self, puchase_id):
        return purchases[purchase_id]

    # def delete(self, purchase_id):
    #     if purchase_id in purchases:
    #         del purchases[purchase_id]
    #     return '', 204

class PurchaseListResource(Resource):
    def get(self):
        return purchases

    def post(self):
        # Get arguments from request
        args = purchase_parser.parse_args()

        # Get next purchase id
        purchase_id = len(purchases)+1

        if not CheckAmountSyntax(str(args['amount'])):
            abort(400, message="Invalid amount syntax")

        # if not CheckDateSyntax(args['date']):
        #     abort(400, message="Invalid date syntax. Must be yyyy-mm-dd.")

        # If the request contains a category
        if 'category' in args:
            purchase = {
                'name': args['name'],
                'amount': args['amount'],
                'category': args['category'],
                'date': args['date']
            }

            # If the category exists in categories list, add purchase to category
            if args['category'] in categories:
                category = categories[args['category']]
                cat_purchases = category['purchases']
                cat_purchases.append(purchase)
            # Otherwise, abort and warn user that the category doesn't exist
            else:
                abort(404, message="Category {} doesn't exist".format(args['category']))

        # If the request doesn't contain a category
        else:
            purchase = {
                'name': args['name'],
                'amount': args['amount'],
                'category': 'uncategorized',
                'date': args['date']
            }

        # Add purchase to purchase list and return it
        purchases[purchase_id] = purchase
        return purchases[purchase_id], 201

class CategoryResource(Resource):
    def get(self, cat_name):
        return categories[cat_name]

    def put(self, cat_name):
        if cat_name.lower() == "uncategorized":
            abort(403, message="Cannot modify the 'uncategorized' category")

        args = cat_put_parser.parse_args()

        if not CheckAmountSyntax(str(args['budget'])):
            abort(400, message="Invalid budget syntax")

        cat = categories[cat_name]
        cat['budget'] = args['budget']

        return cat, 201

    def delete(self, cat_name):
        # Can't delete uncategorized category
        if cat_name.lower() == "uncategorized":
            abort(403, message="Cannot delete the 'uncategorized' category")
        # If the category exists
        elif cat_name in categories:
            # Get uncategorized purchase list
            uncat = categories['uncategorized']
            uncat_purch = uncat['purchases']
            # For each purchase in purchase list
            for purch in purchases:
                # If the purchase's category is the one being deleted
                if purchases[purch]["category"] == cat_name:
                    # Set purchase category to uncategorized
                    purchases[purch]["category"] = "uncategorized";
                    uncat_purch.append(purchases[purch])
            # Delete category from list
            del categories[cat_name]
            return '', 204
        # Otherwise, return
        return '', 204

class CategoryListResource(Resource):
    def get(self):
        # Return a list comprehension of category list --> Easier for processing in js
        return [categories[index] for index in categories]

    def post(self):
        args = cat_parser.parse_args()
        if args['name'].lower() == 'uncategorized':
            abort(403, message="Cannot add a category with name 'uncategorized'")

        if not CheckAmountSyntax(str(args['budget'])):
            abort(400, message="Invalid budget syntax")

        if 'budget' in args:
            category = {
                'name': args['name'],
                'budget': args['budget'],
                'purchases': []
            }

        else:
            category = {
                'name': args['name'],
                'budget': None,
                'purchases': []
            }
        categories[category['name']] = category

        # Return a list comprehension of category list --> Easier for processing in js
        return [categories[index] for index in categories], 201

def CheckAmountSyntax(amount):
    amountRegex = re.compile("^\$?(?=\d|\.)\d*\.?\d{0,2}$")
    if amountRegex.match(amount) is not None:
        return True
    return False

# def CheckDateSyntax(date):
#     dateRegex = re.compile("^\d\d\d\d\-\d\d\-\d\d$")
#     if dateRegex.match(date) is not None:
#         return True
#     return False

api.add_resource(PurchaseListResource, '/purchases')
api.add_resource(PurchaseResource, '/purchases/<int:purchase_id>')
api.add_resource(CategoryListResource, '/cats')
api.add_resource(CategoryResource, '/cats/<string:cat_name>')

#---------------------------------------------------------
# Front end:

@app.route("/")
def home():
    # if request.method == "POST":
        # catName = request.form["edit-button"]
        # return redirect(url_for('category', cat_name=catName))
    cat_uncategorized = {
        'name': 'uncategorized',
        'budget': None,
        'purchases': []
    }

    #Add to categories list
    categories['uncategorized'] = cat_uncategorized
    return render_template("home.html")

if __name__ == "__main__":
	app.run(debug=True)
