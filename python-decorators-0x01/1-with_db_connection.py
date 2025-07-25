import sqlite3
import functools

def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')  # Automatically open connection
        try:
            return func(conn, *args, **kwargs)  # Pass connection as first argument
        finally:
            conn.close()  # Ensure connection is closed afterward
    return wrapper

@with_db_connection
def get_user_by_id(conn, user_id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()

# ✅ Test the decorated function
if __name__ == "__main__":
    user = get_user_by_id(user_id=1)
    print(user)
