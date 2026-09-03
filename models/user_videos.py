import sqlite3
from datetime import datetime

def save_user_video(user_id, file_path):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO user_videos (user_id, file_path, upload_date)
        VALUES (?, ?, ?)
    """, (user_id, file_path, datetime.now().isoformat()))
    conn.commit()
    conn.close()

def get_user_videos(user_id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user_videos WHERE user_id = ?", (user_id,))
    videos = cursor.fetchall()
    conn.close()
    return videos