import mysql.connector.pooling
from mysql.connector import Error

# Database configuration
db_config = {
    "host": 'sql11.freemysqlhosting.net',
    "database": 'sql11692048',
    "user": 'sql11692048',
    "password": 'GdVpfiC7JD',
    "port": '3306',
    "pool_name": "mypool",
    "pool_size": 5
}

# Initialize the connection pool
connection_pool = mysql.connector.pooling.MySQLConnectionPool(**db_config)


def execute_query(query, values=None, table='zodiac_sign_feedback'):
    """
    Executes the given SQL query with optional parameters and returns the result.
    :param query: The SQL query to execute.
    :param values: Optional values for parameterized query.
    :param table: The name of the table to execute the query on.
    :return: Result of the query execution.
    """
    connection = connection_pool.get_connection()
    result = None
    try:
        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)
            if values:
                cursor.execute(query, values)
            else:
                cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
    except Error as e:
        print(f"Error executing query: {e}")
    finally:
        if connection and connection.is_connected():
            connection.close()
    return result or []  # Return an empty list if result is None


# Function to save feedback to the database
def save_feedback_to_database(name, comment, rating, zodiac_sign, table='zodiac_sign_feedback'):
    try:
        connection = connection_pool.get_connection()
        if connection:
            cursor = connection.cursor()
            insert_query = f"INSERT INTO {table} (name, comment, rating, zodiac_sign) VALUES (%s, %s, %s, %s)"
            cursor.execute(insert_query, (name, comment, rating, zodiac_sign))
            connection.commit()
            print("Feedback saved successfully")
    except Error as e:
        print(f"Error saving feedback to database: {e}")
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")

# Function to retrieve feedback from the database
def get_feedback_from_database(table='zodiac_sign_feedback'):
    feedback_data = []
    connection = None  # Initialize connection variable
    try:
        connection = connection_pool.get_connection()  # Assign connection within try block
        if connection:
            cursor = connection.cursor(dictionary=True)
            select_query = f"SELECT name, comment, rating, zodiac_sign FROM {table}"
            cursor.execute(select_query)
            feedback_data = cursor.fetchall()
    except Error as e:
        print(f"Error fetching feedback from database: {e}")
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")
    return feedback_data

# Additional database operations/functions can be added here
