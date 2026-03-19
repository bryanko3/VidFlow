from core.database import connect

def toggle_like(video_id, user_id):
    db = connect()
    c = db.cursor()

    existing = c.execute("""
        SELECT id
        FROM likes
        WHERE video_id=? AND user_id=?
    """, (video_id, user_id)).fetchone()

    if existing:
        c.execute("DELETE FROM likes WHERE id=?", (existing["id"],))
        db.commit()
        return False
    else:
        c.execute("INSERT INTO likes(video_id,user_id) VALUES(?,?)", (video_id, user_id))
        db.commit()
        return True

def get_like_count(video_id):
    db = connect()
    c = db.cursor()
    r = c.execute("SELECT COUNT(*) as total FROM likes WHERE video_id=?", (video_id,)).fetchone()
    return r["total"]

def user_liked(video_id, user_id):
    if not user_id:
        return False
    db = connect()
    c = db.cursor()
    r = c.execute("SELECT id FROM likes WHERE video_id=? AND user_id=?", (video_id, user_id)).fetchone()
    return r is not None

def get_liked_videos_by_user(user_id):
    db = connect()
    videos = db.execute("""
        SELECT 
            videos.*,
            categories.name as category,
            (SELECT COUNT(*) FROM likes WHERE video_id = videos.id) as likes
        FROM likes
        JOIN videos ON videos.id = likes.video_id
        LEFT JOIN categories ON categories.id = videos.category_id
        WHERE likes.user_id = ?
        ORDER BY likes.created_at DESC
    """, (user_id,)).fetchall()
    db.close()
    return videos