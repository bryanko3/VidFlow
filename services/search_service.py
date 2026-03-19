from core.database import connect

def search_videos(q, category_ids=None):
    db = connect()
    query = """
        SELECT videos.*, users.username, categories.name as category, COUNT(likes.id) as likes
        FROM videos
        JOIN users ON users.id = videos.user_id
        LEFT JOIN categories ON categories.id = videos.category_id
        LEFT JOIN likes ON likes.video_id = videos.id
    """
    conditions = []
    params = []

    if q:
        conditions.append("videos.title LIKE ?")
        params.append(f"%{q}%")

    if category_ids:
        placeholders = ",".join("?" for _ in category_ids)
        conditions.append(f"videos.category_id IN ({placeholders})")
        params.extend(category_ids)

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    query += " GROUP BY videos.id ORDER BY videos.created_at DESC"

    videos = db.execute(query, params).fetchall()
    db.close()
    return videos