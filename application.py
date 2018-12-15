from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp
from helpers import *

import datetime
import time
import hashlib
import gnupg

# configure application
app = Flask(__name__)

# ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

# custom filter
app.jinja_env.filters["usd"] = usd

# configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# configure CS50 Library to use SQLite database
db = SQL("sqlite:///passwordVault.db")

@app.route("/")
@login_required
def index():
    portfolio = db.execute("SELECT login, id, key \
                                    FROM portfolio WHERE name = :name", \
                                    name=session["user_id"])
    return render_template("index.html", infos=portfolio)

@app.route("/remove", methods=["GET", "POST"])
@login_required
def remove():
    if request.method == "POST":
        if not request.form.get("passwd"):
            return apology("must provide your password")
        elif not request.form.get("id"):
            return apology("must provide a password to remove")
        else:
            rows = db.execute("SELECT * FROM users WHERE id = :id", id=session["user_id"])
            if len(rows) != 1 or not pwd_context.verify(request.form.get("passwd"), rows[0]["hash"]):
                return apology("invalid password!!")
            else:
                db.execute("DELETE FROM portfolio WHERE (id) = (:id)", id=request.form.get("id"))
                portfolio = db.execute("SELECT login, id, key \
                                        FROM portfolio WHERE name = :name", \
                                        name=session["user_id"])
                return render_template("remove.html", infos=portfolio)
    else:
        portfolio = db.execute("SELECT login, id, key \
                                FROM portfolio WHERE name = :name", \
                                name=session["user_id"])
        return render_template("remove.html", infos=portfolio)



@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    if request.method == "POST":
        if not request.form.get("passwd"):
            return apology("must provide your password")
        elif not request.form.get("login"):
            return apology("must provide a username to encrypt")
        elif not request.form.get("password"):
            return apology("must provide a password to encrypt")
        else:
            rows = db.execute("SELECT * FROM users WHERE id = :id", id=session["user_id"])
            if len(rows) != 1 or not pwd_context.verify(request.form.get("passwd"), rows[0]["hash"]):
                return apology("invalid password!!")
            else:
                login = request.form.get("login")
                password = request.form.get("password")
                passwd = request.form.get("passwd")
                comment = request.form.get("comment")
                if not login:
                    return apology("login required")
                elif not password:
                    return apology("login required")
                gnupghome = '/usr/bin/gpg'
                gpg = gnupg.GPG(gnupghome)
                afile = str(gpg.encrypt(password,
                              symmetric='AES256', passphrase=passwd, encrypt=False))
                
                db.execute("INSERT INTO portfolio (login, mfile, name, key) VALUES(:login, :mfile, :name, :key)", login=request.form.get("login"), mfile=afile, name=session["user_id"], key=comment)
                               
                return redirect(url_for("index"))
    else:
        return render_template("add.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in."""
    session.clear()
    if request.method == "POST":
        if not request.form.get("username"):
            return apology("must provide username")
        elif not request.form.get("password"):
            return apology("must provide password")
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))
        if len(rows) != 1 or not pwd_context.verify(request.form.get("password"), rows[0]["hash"]):
            return apology("invalid username and/or password")
        session["user_id"] = rows[0]["id"]
        return redirect(url_for("index"))
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out."""
    session.clear()
    return redirect(url_for("login"))

@app.route("/decrypt", methods=["GET", "POST"])
@login_required
def decrypt():
    if request.method == "POST":
        rows = db.execute("SELECT * FROM portfolio WHERE id = :id", id=request.form.get("id"))
        if not rows:
            return apology("Invalid Symbol")
        password = rows[0]["mfile"]
        passwd = request.form.get("passwd")
        gnupghome = '/usr/bin/gpg'
        gpg = gnupg.GPG(gnupghome)
        afile = gpg.decrypt_file(password, passphrase=passwd)
        return render_template("decrypt.html", password=afile, login = rows[0]["login"], comment = rows[0]["key"])
    else:
        return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user."""

    if request.method == "POST":
        if not request.form.get("username"):
            return apology("You must provide a username")
        elif not request.form.get("password"):
            return apology("You must provide a password")
        elif not request.form.get("password2"):
            return apology("You must confirm your password")
        else:
            if request.form.get("password") != request.form.get("password2"):
                return apology("Password don\'t match")
            else:
                db.execute("INSERT INTO users (hash, username) Values(:hash_obj, :username)",
                hash_obj = pwd_context.hash(request.form.get("password")),
                username = request.form.get("username"))
                return render_template("login.html")
    else:
        return render_template("register.html")

@login_required
@app.route("/password", methods=["GET", "POST"])
def password():
    """Change Password."""

    if request.method == "POST":
        if not request.form.get("password"):
            return apology("You must provide a password")
        elif not request.form.get("password2"):
            return apology("You must confirm your password")
        else:
            if request.form.get("password") != request.form.get("password2"):
                return apology("Password don\'t match")
            else:
                db.execute("UPDATE users SET hash=:hash_obj WHERE id=:id", id=session["user_id"], hash_obj = pwd_context.hash(request.form.get("password")))
                return redirect(url_for("login"))
    else:
        return render_template("password.html")
