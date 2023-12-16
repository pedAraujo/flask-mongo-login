from flask import session, render_template, Blueprint, flash
from .auth.routes import login_required

main = Blueprint("main", __name__)


@main.route("/")
@main.route("/index/")
@login_required
def index():
    error = None
    if "username" in session:
        return render_template("index.html", username=session["username"])
    error = "You must be logged in to view this page."
    flash(error)
    return render_template("index.html", error=error)
