import sqlite3

def get_all_videos(stroke=None):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    if stroke:
        cursor.execute("SELECT * FROM videos WHERE stroke = ?", (stroke,))
    else:
        cursor.execute("SELECT * FROM videos")

    videos = cursor.fetchall()
    conn.close()
    return videos

def get_video(video_id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM videos WHERE id = ?", (video_id,))
    video = cursor.fetchone()
    conn.close()
    return video