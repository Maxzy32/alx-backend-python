import seed

def stream_user_ages():
    """
    Generator function that yields user ages one by one.
    Connects to the ALX_prodev database, queries the user_data table,
    and yields the 'age' field for each user.
    """
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT age FROM user_data")
    # Use one loop to yield each row's age
    for row in cursor:
        yield row['age']
    cursor.close()
    connection.close()
    return  # explicit return statement

def calculate_average_age():
    """
    Uses the stream_user_ages generator to calculate the average age of users.
    This function iterates through all ages (one loop) and computes the aggregate result.
    """
    total_age = 0
    count = 0
    # Second loop: process each age from the generator
    for age in stream_user_ages():
        total_age += float(age)
        count += 1
    if count == 0:
        print("Average age of users: 0")
    else:
        average = total_age / count
        print(f"Average age of users: {average}")

if __name__ == '__main__':
    calculate_average_age()
