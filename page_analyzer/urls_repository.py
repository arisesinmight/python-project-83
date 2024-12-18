from contextlib import closing
from datetime import date

import psycopg2
import requests
from bs4 import BeautifulSoup
from psycopg2.extras import RealDictCursor


def get_(url, content):
    response = requests.get(url['name'])
    html_body = response.text
    soup = BeautifulSoup(html_body, 'html.parser')
    if content == 'status_code':
        return response.status_code
    if content == 'h1':
        if soup.h1:
            return soup.h1.string
    if content == 'title':
        if soup.title:
            return soup.title.string
    if content == 'description':
        meta = soup.select('meta[name="description"]')
        for row in meta:
            desc = row.get('content')
            if desc:
                return desc
    return None


class UrlsRepository:
    def __init__(self, db_url):
        self.db_url = db_url

    def get_connection(self):
        return closing(psycopg2.connect(self.db_url))

    def find_by(self, id):
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

    def get_summary_data(self):
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    "SELECT\
                    urls.id, urls.name, url_checks.status_code,\
                    url_checks.created_at as last_check\
                    FROM urls\
                    LEFT JOIN url_checks ON urls.id = url_checks.url_id\
                    GROUP BY urls.id,\
                    url_checks.status_code, url_checks.created_at\
                    ORDER BY urls.id DESC;"
                )
                return cur.fetchall()

    @staticmethod
    def check_status(url):
        try:
            response = requests.get(url['name'])
            response.raise_for_status()
        except requests.exceptions.ConnectionError:
            return
        return True

    def make_check(self, url):
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO url_checks (\
                    url_id, status_code, h1, title, description, created_at)\
                    VALUES (%s, %s, %s, %s, %s, %s)",
                    (url['id'],
                     get_(url, 'status_code'),
                     get_(url, 'h1'),
                     get_(url, 'title'),
                     get_(url, 'description'),
                     date.today())
                )
            conn.commit()
        return

    def get_check_results(self, url):
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    "SELECT id, url_id, status_code,\
                    h1, title, description, created_at\
                    FROM url_checks\
                    WHERE url_id = %s ORDER BY id DESC",
                    (url['id'],)
                )
                return cur.fetchall()
