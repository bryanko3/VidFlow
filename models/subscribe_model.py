from core.database import connect

def is_subscribed(user_id, channel_id):

    db = connect()
    c = db.cursor()

    c.execute("""
    SELECT id FROM subscriptions
    WHERE user_id=? AND channel_id=?
    """,(user_id,channel_id))

    result = c.fetchone()

    db.close()

    return result is not None


def toggle_subscription(user_id, channel_id):

    db = connect()
    c = db.cursor()

    c.execute("""
    SELECT id FROM subscriptions
    WHERE user_id=? AND channel_id=?
    """,(user_id,channel_id))

    sub = c.fetchone()

    if sub:

        c.execute("""
        DELETE FROM subscriptions
        WHERE id=?
        """,(sub["id"],))

        db.commit()
        db.close()

        return False

    else:

        c.execute("""
        INSERT INTO subscriptions(user_id,channel_id)
        VALUES(?,?)
        """,(user_id,channel_id))

        db.commit()
        db.close()

        return True


def get_subscribers(channel_id):

    db = connect()
    c = db.cursor()

    r = c.execute("""
    SELECT COUNT(*) as total
    FROM subscriptions
    WHERE channel_id=?
    """,(channel_id,)).fetchone()

    return r["total"]


def get_subscribed_channels(user_id):

    db = connect()
    c = db.cursor()

    return c.execute("""

    SELECT users.*,

    (SELECT COUNT(*) 
     FROM subscriptions 
     WHERE channel_id=users.id) as subscribers,

    (SELECT COUNT(*)
     FROM likes
     JOIN videos ON videos.id = likes.video_id
     WHERE videos.user_id = users.id) as total_likes

    FROM subscriptions

    JOIN users
    ON users.id = subscriptions.channel_id

    WHERE subscriptions.user_id=?

    """,(user_id,)).fetchall()