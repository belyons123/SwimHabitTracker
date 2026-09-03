#Main app file
#Author: Ben Lyons
#Date created: 6/27/2026

import sqlite3
import os
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, redirect, session
from models.user import create_user, verify_user, get_username
from models.videos import get_all_videos, get_video
from models.user_videos import save_user_video, get_user_videos, get_user_video

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
cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_videos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        file_path TEXT NOT NULL,
        upload_date TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id)
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
    if "user_id" not in session:
        return redirect("/login")

    username = get_username(session["user_id"])
    return render_template("home.html", username=username)

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

#User video upload
UPLOAD_FOLDER = "static/uploads"
ALLOWED_EXTENSIONS = {"mp4", "mov"}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/upload_video", methods=["GET", "POST"])
def upload_video():
    if "user_id" not in session:
        return redirect("/login")

    if request.method == "POST":
        file = request.files.get("video")

        if not file or file.filename == "":
            return render_template("upload_video.html", error="Please select a file.")

        if not allowed_file(file.filename):
            return render_template("upload_video.html", error="Only MP4 or MOV files allowed.")

        filename = secure_filename(file.filename)
        save_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(save_path)

        save_user_video(session["user_id"], f"uploads/{filename}")

        return redirect("/compare_select")

    return render_template("upload_video.html", error=None)

#Video Comparison Selection
@app.route("/compare_select")
def compare_select():
    if "user_id" not in session:
        return redirect("/login")

    user_videos = get_user_videos(session["user_id"])
    pro_videos = get_all_videos()  # from Phase 6

    return render_template("compare_select.html", user_videos=user_videos, pro_videos=pro_videos)

#Side-by-Side Video Comparer
@app.route("/compare_viewer")
def compare_viewer():
    if "user_id" not in session:
        return redirect("/login")

    user_vid = request.args.get("user_vid")
    pro_vid = request.args.get("pro_vid")

    user_video = get_user_video(user_vid)
    pro_video = get_video(pro_vid)

    return render_template("compare_viewer.html", user_video=user_video, pro_video=pro_video)

#- Run the app
if __name__ == "__main__":
    app.run(debug=True)