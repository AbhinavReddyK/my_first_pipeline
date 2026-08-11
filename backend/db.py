"""Postgres connection helper for the sales dashboard API."""

import os

import psycopg2
import psycopg2.extras

PG_CONFIG = {
    "host": "localhost",
    "port": 5433,
    "dbname": "sales_pipeline",
    "user": "postgres",
    "password": os.environ.get("PGPASSWORD"),
}


def get_connection():
    return psycopg2.connect(**PG_CONFIG)


def fetch_all(query: str, params: tuple = ()) -> list[dict]:
    conn = get_connection()
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(query, params)
            return [dict(row) for row in cur.fetchall()]
    finally:
        conn.close()
