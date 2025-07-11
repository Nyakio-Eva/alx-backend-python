import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def stream_users_in_batches(batch_size):
    """
    Generator that yields batches of rows from the user_data table.
    """
    connection = mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "ALX_prodev")
    )
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT * FROM user_data")

    while True:
        rows = cursor.fetchmany(batch_size)
        if not rows:
            break
        yield rows

    cursor.close()
    connection.close()


def batch_processing(batch_size):
    """
    Generator that processes each batch and yields users over age 25.
    """
    for batch in stream_users_in_batches(batch_size):  # Loop 1
        for user in batch:  # Loop 2
            if float(user['age']) > 25:
                yield user
