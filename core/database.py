import sqlite3
from config import Config

def connect():
    conn = sqlite3.connect(Config.DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    db = connect()
    c = db.cursor()

    # users
    c.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        bio TEXT,
        profile_image TEXT,
        profile_status TEXT DEFAULT 'public',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # categories
    c.execute("""
    CREATE TABLE IF NOT EXISTS categories(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT
    )
    """)

    # videos
    c.execute("""
    CREATE TABLE IF NOT EXISTS videos(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        title TEXT,
        description TEXT,
        filename TEXT,
        category_id INTEGER,
        thumbnail TEXT,
        views INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # comments
    c.execute("""
    CREATE TABLE IF NOT EXISTS comments(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        video_id INTEGER,
        user_id INTEGER,
        text TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # likes
    c.execute("""
    CREATE TABLE IF NOT EXISTS likes(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        video_id INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    db.commit()

    # 카테고리 기본 데이터
    categories = [
    "Film & Animation",
    "Gaming",
    "Music",
    "Entertainment",
    "Vlogs & Lifestyle",
    "Education",
    "Science & Technology",
    "News & Politics",
    "Sports & Fitness",
    "Kids & Family",
    "Food & Cooking",
    "Beauty & Fashion",
    "Travel & Events",
    "Business & Finance",
    "Art & Design"
    ]

    c.execute("SELECT COUNT(*) FROM categories")
    if c.fetchone()[0] == 0:
        for cat in categories:
            c.execute("INSERT INTO categories(name) VALUES(?)",(cat,))

    db.commit()

    # subscriptions
    c.execute("""
    CREATE TABLE IF NOT EXISTS subscriptions(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        channel_id INTEGER,
        user_id INTEGER
    )
    """)

    db.commit()
    db.close()