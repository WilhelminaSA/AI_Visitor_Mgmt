import psycopg2

from psycopg2.extras import RealDictCursor

from config.settings import (
    DB_HOST,
    DB_PORT,
    DB_NAME,
    DB_USER,
    DB_PASSWORD
)

# ======================================================
# DATABASE CONNECTION
# ======================================================

def get_connection():

    connection = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

    return connection

# ======================================================
# DICTIONARY CURSOR
# ======================================================

def get_dict_cursor(connection):

    return connection.cursor(
        cursor_factory=RealDictCursor
    )

# ======================================================
# TEST DATABASE CONNECTION
# ======================================================

def test_connection():

    try:

        connection = get_connection()

        print()
        print("[SUCCESS] Database connected successfully")

        connection.close()

    except Exception as error:

        print()
        print("[ERROR] Database connection failed")
        print(error)
