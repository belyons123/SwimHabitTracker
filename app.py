#Main app file
#Author: Ben Lyons
#Date created: 6/27/2026

import sqlite3
from flask import Flask, render_template, request, redirect, session
from models.user import create_user, verify_user

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



#Create the Flask application
app = Flask(__name__)
app.secret_key = "chewie"
@app.route("/") #Root where people will first vist, currently only goes to register for test purposes
def root():
    return redirect("/register")
#- Route 1: Register
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        success = create_user(username, password)
        if not success:
            return "Username already exists. Please choose another one"
        return redirect("/login")
    return render_template("register.html", error ="Username already exists")
#- Route 2: Login
@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user_id = verify_user(username,password)
        if user_id:
            return redirect("/home")
        else:
            return render_template("login.html")
    return render_template("login.html")
#- temporary home page
@app.route("/home")
def home():
    return render_template('home.html')


#*Later, I'll replace this with:
# return render_template("dashboard.html")

#- Run the app
if __name__ == "__main__":
    app.run(debug=True)