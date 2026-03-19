from core.database import connect

def create_user(username,password,profile_image):

    db=connect()
    c=db.cursor()

    c.execute("""
    INSERT INTO users(username,password,profile_image)
    VALUES(?,?,?)
    """,(username,password,profile_image))

    db.commit()
    db.close()

def get_user_by_username(username):
    db = connect()
    c = db.cursor()
    return c.execute("""
        SELECT *
        FROM users
        WHERE username=?
    """, (username,)).fetchone()

def get_user(user_id):
    db = connect()
    c = db.cursor()
    return c.execute("""
        SELECT *
        FROM users
        WHERE id=?
    """, (user_id,)).fetchone()

def update_user_bio(user_id, bio):
    db = connect()
    c = db.cursor()
    c.execute("""
        UPDATE users
        SET bio=?
        WHERE id=?
    """, (bio, user_id))
    db.commit()