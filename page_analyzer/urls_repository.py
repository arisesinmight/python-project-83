import psycopg2
from datetime import date
from psycopg2.extras import RealDictCursor
from contextlib import closing


class UrlsRepository:
    def __init__(self, db_url):
        self.db_url = db_url

    def get_connection(self):
        return closing(psycopg2.connect(self.db_url))

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

    def get_urls_content(self):
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("SELECT * FROM urls ORDER BY id DESC")
                return cur.fetchall()

    def get_full_data(self):
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    "SELECT\
                    urls.id, urls.name,\
                    url_checks.created_at as last_check\
                    FROM urls\
                    LEFT JOIN url_checks ON urls.id = url_checks.url_id\
                    GROUP BY urls.id, url_checks.created_at\
                    ORDER BY urls.id DESC;"
                )
                return cur.fetchall()

    def check(self, url):
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO url_checks (url_id, created_at)\
                    VALUES (%s, %s)",
                    (url['id'], date.today())
                )
            conn.commit()
        return

    def get_check_result(self, url):
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    "SELECT id, url_id, created_at FROM url_checks\
                    WHERE url_id = 1 ORDER BY id DESC",
                    (url['id'],)
                )
                return cur.fetchall()
