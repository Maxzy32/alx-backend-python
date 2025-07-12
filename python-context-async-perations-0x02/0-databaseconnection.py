import sqlite3

class DatabaseConnection:
    def __init__(self, db_name='users.db'):
        self.db_name = db_name
        self.conn = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        return self.conn  # returns the connection object to use inside the `with` block

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()  # ensure connection is closed even if an exception occurs

# === Example usage ===
if __name__ == "__main__":
    with DatabaseConnection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        results = cursor.fetchall()
        for row in results:
            print(row)
