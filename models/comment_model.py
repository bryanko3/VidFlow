from core.database import connect

def add_comment(video_id,user_id,text):

    db = connect()
    c = db.cursor()

    c.execute("""
    INSERT INTO comments(video_id,user_id,text)
    VALUES(?,?,?)
    """,(video_id,user_id,text))

    db.commit()


def delete_comment(comment_id,user_id):

    db = connect()
    c = db.cursor()

    c.execute("""
    DELETE FROM comments
    WHERE id=? AND user_id=?
    """,(comment_id,user_id))

    db.commit()


def get_comments(video_id):

    db = connect()
    c = db.cursor()

    c.execute("""
    SELECT
    comments.*,
    users.username,
    users.profile_image,
    users.profile_status
    FROM comments
    JOIN users ON comments.user_id = users.id
    WHERE comments.video_id = ?
    ORDER BY comments.created_at DESC
    """,(video_id,))

    comments = c.fetchall()

    db.close()

    return comments