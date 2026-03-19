from core.database import connect

def get_categories():

    db = connect()

    c = db.cursor()

    return c.execute("""

    SELECT *

    FROM categories

    """).fetchall()