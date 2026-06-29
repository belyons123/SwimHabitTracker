#User data security file
#Author: Ben Lyons
#Date Created: 6/28/2026

import sqlite3
import hashlib
import os
from datetime import datetime

#Users after they're loaded from the database
class User:
    def __init__(self, id, username, hashed_password, salt, created_at):
        self.id = id
        self.username = username
        self.hashed_password = hashed_password
        self.salt = salt
        self.created_at = created_at

#Password Hashing Function
def hash_password(password, salt):
    return hashlib.sha256((password+salt).encode()).hexdigest()

#Generate random salt
def generate_salt():
    return os.urandom(16).hex()

#Create the new user
def create_user(username, password):
    salt = generate_salt()
    hashed_password = hash_password(password, salt)
    created_at = datetime.now(datetime.UTC)

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO users (username, hashed_password, salt, created_at)
        VALUES (?, ?, ?, ?)
    """, (username, hashed_password, salt, created_at))

    conn.commit()
    conn.close()

#Verify a login attempt from users
def verify_user(username, password):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT id, username, hashed_password, salt FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()
    conn.close()

    if row is None:
        return None  # user not found

    user_id, username, stored_hash, salt = row

    attempted_hash = hash_password(password, salt)

    if attempted_hash == stored_hash:
        return user_id  # login success
    else:
        return None  # login failed