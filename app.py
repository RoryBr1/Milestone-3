import os
from datetime import date
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env

today = date.today()

app = Flask(__name__)

# Flask Config
app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


# Show recipes; displays recipes on homepage
@app.route("/")
@app.route("/get_recipes")
def get_recipes():
    # Find all recipes in the collection, "recipes":
    recipes = list(mongo.db.recipes.find())
    # Find all categories in the collection, "categories"
    # (used for the sort-by-category dropdown):
    categories = list(mongo.db.categories.find())
    # Return the recipes page with all recipes:
    return render_template(
        "recipes.html", recipes=recipes,
        categories=categories)


# Search functionality:
@app.route("/search", methods=["GET", "POST"])
def search():
    # Request the search query from the search input:
    query = request.form.get("query")
    # Find all recipes that match the query:
    recipes = list(mongo.db.recipes.find({"$text": {"$search": query}}))
    # Find all categories in the collection, "categories"
    # (used for the sort-by-category dropdown):
    categories = list(mongo.db.categories.find())
    # Display flash message:
    flash("Showing results for " + "'" + query + "'")
    # Return the recipes page with relevant recipes:
    return render_template(
        "recipes.html", recipes=recipes, categories=categories)


# Sort-by-category functionality:
@app.route("/category_filter/<category>", methods=['GET', 'POST'])
def category_filter(category):
    # Find all recipes where the category_name matches the selection:
    recipes = list(mongo.db.recipes.find({"category_name": category}))
    # Find all categories in the collection, "categories"
    # (used for the sort-by-category dropdown):
    categories = list(mongo.db.categories.find())
    # Display flash message:
    flash("Showing all recipes in category " + "'" + category + "'")
    # Return the recipes page with relevant recipes:
    return render_template(
        "recipes.html", recipes=recipes, categories=categories)


# Admin login authentication
# (taken from CodeInstitute Flask-MongoDB mini-project):
@app.route("/admin_login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        # check if username exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            # ensure hashed password matches user input
            if check_password_hash(
                    existing_user["password"], request.form.get("password")):
                session["user"] = request.form.get("username").lower()
                flash("Logged in as {}".format(
                    request.form.get("username")))
                return redirect(url_for(
                    "get_recipes"))
            else:
                # invalid password match
                flash("Incorrect Password")
                return redirect(url_for("admin_login"))

        else:
            # username doesn't exist
            flash("Incorrect Username")
            return redirect(url_for("admin_login"))

    return render_template("admin-login.html")


# Register a new user (taken from CodeInstitute Flask-MongoDB mini-project):
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # check if username already exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("Username already exists")
            return redirect(url_for("register"))

        register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password"))
        }
        mongo.db.users.insert_one(register)

        # put the new user into 'session' cookie
        session["user"] = request.form.get("username").lower()
        flash("Registration Successful!")
        return redirect(url_for("profile", username=session["user"]))

    return render_template("admin-login.html")


# Logout function (taken from CodeInstitute Flask-MongoDB mini-project):
@app.route("/logout")
def logout():
    # remove user from session cookie
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("get_recipes"))


# Add Recipe functionality:
@app.route("/add_recipe", methods=["GET", "POST"])
def add_recipe():
    # Create recipe object by requesting form data
    # and assigning it in key-value pairs
    if request.method == "POST":
        recipe = {
            "recipe_name": request.form.get("recipe_name").title(),
            "prep_time": request.form.get("prep_time"),
            "category_name": request.form.get("category_name"),
            "ingredients": request.form.get("ingredients"),
            "recipe_instructions": request.form.get("recipe_instructions"),
            "img_url": request.form.get("img_url"),
            "added_by": session["user"],
            "added_on": today.strftime("%B %d, %Y")
        }
        # recipe_name is used in the flash message:
        recipe_name = request.form.get("recipe_name").title()
        # Insert the recipe object into the recipes collection:
        mongo.db.recipes.insert_one(recipe)
        # Display flash image:
        flash("'" + recipe_name + "'" + " added successfully.")
        # Return the recipes page:
        return redirect(url_for("get_recipes"))

    categories = mongo.db.categories.find()
    prep_times = mongo.db.prep_times.find()
    return render_template(
        "add-recipe.html", categories=categories,
        prep_times=prep_times)


# Edit recipe functionality:
@app.route("/edit_recipe/<recipe_id>", methods=["GET", "POST"])
def edit_recipe(recipe_id):
    if request.method == "POST":
        recipe_name = request.form.get("recipe_name").title()
        # Retrieve the edited data from the form on edit-recipe page,
        # and assign it to the submit object:
        submit = {
            "recipe_name": request.form.get("recipe_name").title(),
            "prep_time": request.form.get("prep_time"),
            "category_name": request.form.get("category_name"),
            "ingredients": request.form.get("ingredients"),
            "recipe_instructions": request.form.get("recipe_instructions"),
            "img_url": request.form.get("img_url"),
            "added_by": session["user"],
            "added_on": today.strftime("%B %d, %Y")
        }
        # Update the object with relevant ObjectId in the "recipes"
        # collection, with the new data in the "submit" object:
        mongo.db.recipes.update({"_id": ObjectId(recipe_id)}, submit)
        # Display flash message
        flash("'" + recipe_name + "'" + " has been updated")
        # Show the updated recipe:
        return redirect(url_for("show_recipe", recipe_id=recipe_id))

    recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    categories = mongo.db.categories.find().sort("category_name", 1)
    prep_times = mongo.db.prep_times.find()
    return render_template(
        "edit-recipe.html", recipe=recipe,
        categories=categories, prep_times=prep_times)


# Delete recipe functionality:
@app.route("/delete_recipe/<recipe_id>/<recipe_name>")
def delete_recipe(recipe_id, recipe_name):
    # Remove recipe with matching _id from the "recipes" collection:
    mongo.db.recipes.remove({"_id": ObjectId(recipe_id)})
    flash("'" + recipe_name + "'" + " has been deleted")
    return redirect(url_for("get_recipes"))


# Show-recipe page:
@app.route("/show_recipe/<recipe_id>")
def show_recipe(recipe_id):
    # Define "recipe" as the recipe with _id of selection:
    recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    # Load show-recipe.html with the recipe object:
    return render_template("show-recipe.html", recipe=recipe)


# Show-categories page; displays all categories to admin:
@app.route("/show_categories")
def show_categories():
    # Find all categories in the "categories" collection:
    categories = mongo.db.categories.find()
    # Load show-categories with all categories:
    return render_template("show-categories.html", categories=categories)


# Rename category functionality:
@app.route("/rename_category/<category_id>", methods=["GET", "POST"])
def rename_category(category_id):
    if request.method == "POST":
        # Request form data from the form on the Rename modal:
        submit = request.form.get("rename_category").title()
        # Update the relevant category's name:
        mongo.db.categories.update(
            {"_id": ObjectId(category_id)}, {"category_name": submit})

    # Display flash message:
    flash("Category has been renamed to " + "'" + submit + "'")
    return redirect(url_for("show_categories"))


# Delete category functionality:
@app.route("/delete_category/<category_id>/<category_name>")
def delete_category(category_id, category_name):
    # Remove the category from the "categories" collection:
    mongo.db.categories.remove({"_id": ObjectId(category_id)})
    # Display flash message:
    flash(category_name + " has been deleted")
    # Show all categories:
    return redirect(url_for("show_categories"))


# Add category functionality:
@app.route("/add_category", methods=["GET", "POST"])
def add_category():
    # Request data from the form on show-categories page,
    # and assign to "category" variable:
    if request.method == "POST":
        category = {
            "category_name": request.form.get("category_name").title(),
        }
        category_name = request.form.get("category_name").title()
        # Insert the "category" variable to the "categories" collection:
        mongo.db.categories.insert(category)
        # Display flash message:
        flash(category_name + " added successfully.")
        return redirect(url_for("show_categories"))

    return redirect(url_for("show_categories"))


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=False)
