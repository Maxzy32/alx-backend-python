import time
import sqlite3
import functools

# === Reuse your with_db_connection from the previous task ===
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper

# === retry_on_failure decorator ===
def retry_on_failure(retries=3, delay=2):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 0
            while attempt < retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempt += 1
                    print(f"[Retry {attempt}] Error: {e}")
                    if attempt == retries:
                        raise
                    time.sleep(delay)
        return wrapper
    return decorator

# === Decorated function ===
@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

# === Run example ===
if __name__ == "__main__":
    users = fetch_users_with_retry()
    print(users)
