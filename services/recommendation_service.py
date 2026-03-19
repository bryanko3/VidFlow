from core.database import connect

def get_recommended():

    db = connect()

    c = db.cursor()

    return c.execute("""

    SELECT *

    FROM videos

    ORDER BY views DESC

    LIMIT 10

    """).fetchall()