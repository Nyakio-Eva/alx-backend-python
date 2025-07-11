import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def paginate_users(page_size, offset):
    """
    Fetch a page of users with a given offset and limit (page size).
    """
    connection = mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "ALX_prodev")
    )
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT * FROM user_data LIMIT %s OFFSET %s", (page_size, offset))
    users = cursor.fetchall()

    cursor.close()
    connection.close()
    return users


def lazy_paginate(page_size):
    """
    Generator that lazily fetches users page by page using a single loop.
    """
    offset = 0
    while True:  # Only one loop allowed
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size
