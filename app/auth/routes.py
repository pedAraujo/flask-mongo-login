import functools
from bson import ObjectId
from . import auth
from flask import g, redirect, render_template, request, session, url_for, flash
from app.mongo import db
import passlib.hash


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))

        return view(**kwargs)

    return wrapped_view


@auth.before_app_request
def load_user():
    user_id = session.get("user_id")
    user = db.users.find_one({"_id": ObjectId(user_id)})
    if user is None:
        g.user = None
    else:
        user["_id"] = str(user["_id"])
        session["username"] = user["username"]
        g.user = user


@auth.route("/login/", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user_in_db = db.users.find_one({"username": username})
        if not user_in_db or not passlib.hash.sha256_crypt.verify(
            password, user_in_db["password"]
        ):
            error = "Invalid username or password"
            flash(error)
            render_template("login.html", error=error)
        else:
            user_in_db["_id"] = str(user_in_db["_id"])
            session["user_id"] = str(user_in_db["_id"])
            return redirect(url_for("main.index"))
    return render_template("login.html", error=error)


@auth.route("/logout/")
def logout():
    session.clear()
    return redirect(url_for("main.index"))


@auth.route("/register/", methods=("GET", "POST"))
def register():
    error = None
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        user_in_db = db.users.find_one({"username": username})

        if user_in_db:
            error = f"User {username} is already registered."
        if not username:
            error = "Username is required."
        elif not password:
            error = "Password is required."

        if error is None:
            try:
                password = passlib.hash.sha256_crypt.hash(password)
                new_user = {"username": username, "email": email, "password": password}
                db.users.insert_one(new_user)
                flash("User registered successfully")
                return redirect(url_for("auth.login"))
            except Exception as e:
                error = f"Unable to register user {username}: {e}"
        else:
            flash(error)
            return render_template("register.html", error=error)
    return render_template("register.html")
