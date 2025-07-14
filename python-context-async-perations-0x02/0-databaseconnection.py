import sqlite3

# Custom context manager class
class DatabaseConnection:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        return self.conn  # Returned object is assigned to 'conn' in the with block

    def __exit__(self, exc_type, exc_value, traceback):
        if self.conn:
            self.conn.close()

# Use the context manager to query the database
with DatabaseConnection('users.db') as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    results = cursor.fetchall()
    print(results)
