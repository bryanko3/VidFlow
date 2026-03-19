from core.database import connect

def create_video(user_id, title, filename, category, description="", thumbnail=None):
    db = connect()
    c = db.cursor()
    c.execute("""
        INSERT INTO videos(user_id, title, filename, category_id, description, thumbnail)
        VALUES(?,?,?,?,?,?)
    """, (user_id, title, filename, category, description, thumbnail))
    db.commit()


def get_video(video_id):
    db = connect()
    video = db.execute("""
        SELECT
            videos.*,
            users.username,
            categories.name as category,
            (SELECT COUNT(*) FROM likes WHERE video_id = videos.id) as likes
        FROM videos
        JOIN users ON users.id = videos.user_id
        LEFT JOIN categories ON categories.id = videos.category_id
        WHERE videos.id = ?
    """, (video_id,)).fetchone()
    db.close()
    return video


def increase_views(video_id):

    db=connect()
    c=db.cursor()

    c.execute("""

    UPDATE videos
    SET views=views+1
    WHERE id=?

    """,(video_id,))

    db.commit()


def get_latest_videos():

    db = connect()

    videos = db.execute("""
        SELECT 
            videos.*,
            users.username,
            categories.name as category,
            COUNT(likes.id) as likes
        FROM videos
        JOIN users ON users.id = videos.user_id
        LEFT JOIN categories ON categories.id = videos.category_id
        LEFT JOIN likes ON likes.video_id = videos.id
        GROUP BY videos.id
        ORDER BY videos.created_at DESC
    """).fetchall()

    db.close()

    return videos


def get_user_videos(user_id, sort="latest"):

    db = connect()
    c = db.cursor()

    order = "videos.created_at DESC"
    if sort == "views":
        order = "videos.views DESC"
    elif sort == "oldest":
        order = "videos.created_at ASC"

    videos = c.execute(f"""
        SELECT 
            videos.*,
            categories.name as category,
            (SELECT COUNT(*) FROM likes WHERE video_id=videos.id) as likes
        FROM videos
        LEFT JOIN categories ON categories.id = videos.category_id
        WHERE videos.user_id = ?
        ORDER BY {order}
    """, (user_id,)).fetchall()

    db.close()
    return videos


def get_total_likes_by_user(user_id):

    db=connect()
    c=db.cursor()

    r=c.execute("""

    SELECT COUNT(*) as total

    FROM likes

    JOIN videos
    ON videos.id=likes.video_id

    WHERE videos.user_id=?

    """,(user_id,)).fetchone()

    return r["total"]


def delete_video(video_id,user_id):

    db=connect()
    c=db.cursor()

    c.execute("""

    DELETE FROM videos
    WHERE id=? AND user_id=?

    """,(video_id,user_id))

    db.commit()