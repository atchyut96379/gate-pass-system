import os
import psycopg2

def get_connection():
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        raise Exception("DATABASE_URL not set!")

    conn = psycopg2.connect(database_url)
    return conn


def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    # USERS TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        userid SERIAL PRIMARY KEY,
        name VARCHAR(100),
        email VARCHAR(100),
        password VARCHAR(200),
        role VARCHAR(50),
        phone VARCHAR(20),
        flatnumber VARCHAR(20),
        isactive BOOLEAN DEFAULT TRUE
    );
    """)

    # VISITORS TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS visitors (
        visitorid SERIAL PRIMARY KEY,
        visitorname VARCHAR(100),
        visitorphone VARCHAR(20),
        purpose VARCHAR(100),
        flatnumber VARCHAR(20),
        otp VARCHAR(10),
        otpexpiry TIMESTAMP,
        status VARCHAR(20),
        createdby INTEGER,
        createdat TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # ENTRY LOGS TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS entrylogs (
        logid SERIAL PRIMARY KEY,
        visitorid INTEGER REFERENCES visitors(visitorid),
        verifiedby INTEGER REFERENCES users(userid),
        status VARCHAR(20),
        verifiedat TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    conn.commit()
    cursor.close()
    conn.close()
