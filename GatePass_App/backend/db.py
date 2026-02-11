import os
import psycopg2

DATABASE_URL = os.getenv("DATABASE_URL")

conn = psycopg2.connect(DATABASE_URL)
conn.autocommit = True

cursor = conn.cursor()

def create_tables():
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            email VARCHAR(100) UNIQUE,
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
