import os
import psycopg2

def get_connection():
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        raise Exception("DATABASE_URL not set!")

    conn = psycopg2.connect(database_url)
    return conn
