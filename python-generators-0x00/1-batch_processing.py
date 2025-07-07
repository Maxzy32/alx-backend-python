import mysql.connector

def stream_users_in_batches(batch_size):
    """
    Generator function to yield users in batches.
    """
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="ALX_prodev"
        )
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data")

        while True:
            rows = cursor.fetchmany(batch_size)
            if not rows:
                break
            yield rows
        return  # <- explicitly added return

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return  # <- handles early return on error

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def batch_processing(batch_size):
    """
    Processes each batch by filtering users over the age of 25.
    """
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user['age'] > 25:
                print(user)
    return  # <- also valid to include a return here
