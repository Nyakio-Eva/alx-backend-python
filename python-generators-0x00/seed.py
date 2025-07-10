import mysql.connector
from mysql.connector import errorcode
import uuid
import csv
import os

DB_NAME = "ALX_prodev"

TABLE_SCHEMA = """
CREATE TABLE IF NOT EXISTS user_data (
    user_id CHAR(36) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    age DECIMAL NOT NULL,
    INDEX(user_id)
);
"""

def connect_db():
    """Connect to MySQL server (no database selected yet)."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="your_password"  # 🔁 Replace with your MySQL root password
        )
        print("Connected to MySQL server.")
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL: {err}")
        exit(1)

def create_database(connection):
    """Create ALX_prodev database if it does not exist."""
    cursor = connection.cursor()
    try:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        print(f"Database `{DB_NAME}` created or already exists.")
    except mysql.connector.Error as err:
        print(f"Failed to create database: {err}")
        exit(1)
    finally:
        cursor.close()

def connect_to_prodev():
    """Connect to the ALX_prodev database."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="your_password",  # 🔁 Replace with your MySQL root password
            database=DB_NAME
        )
        print(f"Connected to database `{DB_NAME}`.")
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to {DB_NAME}: {err}")
        exit(1)

def create_table(connection):
    """Create user_data table if it doesn't exist."""
    cursor = connection.cursor()
    try:
        cursor.execute(TABLE_SCHEMA)
        print("Table `user_data` created or already exists.")
    except mysql.connector.Error as err:
        print(f"Failed to create table: {err}")
    finally:
        cursor.close()

def insert_data(connection, data):
    """Insert a row of user data if it doesn't already exist."""
    cursor = connection.cursor()
    try:
        # Check for existing email
        cursor.execute("SELECT COUNT(*) FROM user_data WHERE email = %s", (data['email'],))
        if cursor.fetchone()[0] == 0:
            user_id = str(uuid.uuid4())
            cursor.execute(
                "INSERT INTO user_data (user_id, name, email, age) VALUES (%s, %s, %s, %s)",
                (user_id, data['name'], data['email'], data['age'])
            )
            print(f"Inserted: {data['name']} ({data['email']})")
        else:
            print(f"Skipped (duplicate): {data['email']}")
        connection.commit()
    except mysql.connector.Error as err:
        print(f"Error inserting data: {err}")
    finally:
        cursor.close()

def load_csv_and_seed(filepath, connection):
    """Read CSV and insert rows."""
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return
    with open(filepath, mode='r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            insert_data(connection, row)

if __name__ == "__main__":
    conn = connect_db()
    create_database(conn)
    conn.close()

    prodev_conn = connect_to_prodev()
    create_table(prodev_conn)

    csv_file = "user_data.csv"
    load_csv_and_seed(csv_file, prodev_conn)

    prodev_conn.close()
