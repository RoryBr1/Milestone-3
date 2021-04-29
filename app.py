import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env
from datetime import date
today = date.today()

app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route("/")
@app.route("/get_recipes")
def get_recipes():
    recipes = list(mongo.db.recipes.find())
    return render_template("recipes.html", recipes=recipes)


@app.route("/search", methods=["GET", "POST"])
def search():
    query = request.form.get("query")
    recipes = list(mongo.db.recipes.find({"$text": {"$search": query}}))
    flash("Showing results for " + "'" + query + "'")
    return render_template("recipes.html", recipes=recipes)


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


@app.route("/logout")
def logout():
    # remove user from session cookie
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("get_recipes"))


@app.route("/add_recipe", methods=["GET", "POST"])
def add_recipe():
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
        recipe_name = request.form.get("recipe_name").title()
        mongo.db.recipes.insert_one(recipe)
        flash(recipe_name + " added successfully.")
        return redirect(url_for("get_recipes"))

    categories = mongo.db.categories.find()
    prep_times = mongo.db.prep_times.find()
    return render_template("add-recipe.html", categories=categories, prep_times=prep_times)


@app.route("/delete_recipe/<recipe_id>/<recipe_name>")
def delete_recipe(recipe_id, recipe_name):
    mongo.db.recipes.remove({"_id": ObjectId(recipe_id)})
    flash(recipe_name + " has been deleted")
    return redirect(url_for("get_recipes"))


@app.route("/show_recipe/<recipe_id>")
def show_recipe(recipe_id):
    recipe = mongo.db.recipes.find_one({"_id" : ObjectId(recipe_id)}) 
    return render_template("show-recipe.html", recipe=recipe)


@app.route("/show_categories")
def show_categories():
    categories = mongo.db.categories.find()
    return render_template("show-categories.html", categories=categories)


@app.route("/delete_category/<category_id>/<category_name>")
def delete_category(category_id, category_name):
    mongo.db.categories.remove({"_id": ObjectId(category_id)})
    flash(category_name + " has been deleted")
    return redirect(url_for("show_categories"))


@app.route("/add_category", methods=["GET", "POST"])
def add_category():
    if request.method == "POST":
        category = {
            "category_name": request.form.get("category_name").title(),
        }
        category_name = request.form.get("category_name").title()
        mongo.db.categories.insert(category)
        flash(category_name + " added successfully.")
        return redirect(url_for("show_categories"))

    categories = mongo.db.categories.find()
    return redirect(url_for("show_categories"))


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)