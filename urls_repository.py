import psycopg2
from datetime import date
from psycopg2.extras import RealDictCursor



class UrlsRepository:
    def __init__(self, db_url):
        self.db_url = db_url

    def get_connection(self):
        return psycopg2.connect(self.db_url)

    def find(self, id):
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("SELECT * FROM urls WHERE id = %s", (id,))
                return cur.fetchone()

    def get_id(self, name):
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id FROM urls WHERE name = %s", (name,))
                return cur.fetchone()

    def save(self, url):
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO urls (name, created_at) VALUES (%s, %s)",
                    (url, date.today())
                )
        conn.commit()
        return

    def get_content(self):
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("SELECT * FROM urls")
                return cur.fetchall()
