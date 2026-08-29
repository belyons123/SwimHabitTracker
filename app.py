#Main app file
#Author: Ben Lyons
#Date created: 6/27/2026

import sqlite3
from flask import Flask, render_template, request, redirect, session
from models.user import create_user, verify_user
from models.videos import get_all_videos, get_video

#Database establishment
connection = sqlite3.connect("database.db")
cursor = connection.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        hashed_password TEXT NOT NULL,
        salt TEXT NOT NULL,
        created_at TEXT NOT NULL
    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS videos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        stroke TEXT NOT NULL,
        description TEXT,
        file_path TEXT NOT NULL
    )
''')
connection.commit()
connection.close()



#Create the Flask application
app = Flask(__name__)
app.secret_key = "chewie"
@app.route("/") #Root where people will first vist, currently only goes to register for test purposes
def root():
    return redirect("/register")
#Register
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"]
        if not username or not password:
            return render_template("register.html", error="Username and password are required.")
        success = create_user(username, password)
        if not success:
            return render_template("register.html", error="Username already exists. Please choose another one.")
        return redirect("/login")
    return render_template("register.html", error=None)

#Login
@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form["username"].strip()   # trim here too
        password = request.form["password"]
        if not username or not password:
            return render_template("login.html", error="Username and password are required.")
        user_id = verify_user(username, password)
        if user_id:
            session['user_id'] = user_id
            return redirect("/home")
        else:
            return render_template("login.html", error="Invalid username or password.")
    return render_template("login.html", error=None)

#Home Page
@app.route("/home")
def home():
    return render_template('home.html')

#LargerVideo Library
@app.route("/videos")
def video_library():
    if "user_id" not in session:
        return redirect("/login")

    stroke = request.args.get("stroke")  # optional filter
    videos = get_all_videos(stroke)

    return render_template("video_library.html", videos=videos)

#Detail Video
@app.route("/videos/<int:video_id>")
def video_detail(video_id):
    if "user_id" not in session:
        return redirect("/login")

    video = get_video(video_id)
    return render_template("video_detail.html", video=video)

#- Run the app
if __name__ == "__main__":
    app.run(debug=True)