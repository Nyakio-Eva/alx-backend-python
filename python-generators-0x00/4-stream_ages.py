import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def stream_user_ages():
    """
    Generator that yields user ages one by one from the database.
    """
    connection = mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "ALX_prodev")
    )
    cursor = connection.cursor()
    cursor.execute("SELECT age FROM user_data")

    for (age,) in cursor:  # Loop 1
        yield float(age)

    cursor.close()
    connection.close()


def compute_average_age():
    """
    Computes and prints the average age using the stream_user_ages generator.
    """
    total = 0
    count = 0

    for age in stream_user_ages():  # Loop 2
        total += age
        count += 1

    average = total / count if count > 0 else 0
    print(f"Average age of users: {average:.2f}")
