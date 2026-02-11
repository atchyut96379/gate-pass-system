import os
import psycopg2

database_url = os.getenv("DATABASE_URL")
if not database_url:
    raise Exception("DATABASE_URL not set!")

def get_connection():
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        raise Exception("DATABASE_URL not set!")

    conn = psycopg2.connect(database_url)
    return conn

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100),
        email VARCHAR(100),
        password VARCHAR(100),
        phone VARCHAR(20),
        flat_number VARCHAR(20),
        role VARCHAR(20)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS visitors (
        id SERIAL PRIMARY KEY,
        visitor_name VARCHAR(100),
        visitor_phone VARCHAR(20),
        purpose TEXT,
        flat_number VARCHAR(20),
        otp VARCHAR(6),
        status VARCHAR(20),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    conn.commit()
    cursor.close()
    conn.close()
