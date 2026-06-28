import sqlite3
from flask import Flask, render_template


# ------------------------
# Database establishment
# ------------------------
connection = sqlite3.connect('dabase.db')
cursor = connection.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE
    )
''')



# Create the Flask application

app = Flask(__name__)
# -----------------------------
# Routes
# -----------------------------

@app.route("/")
def home():
    return "<h1>Swimmer Habit Tracker</h1><p>Your app is running!</p>"

# Later, I'll replace this with:
# return render_template("dashboard.html")

# -----------------------------
# Run the app
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)