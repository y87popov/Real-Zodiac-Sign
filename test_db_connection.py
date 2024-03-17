import mysql.connector
from mysql.connector import Error

def test_database_connection():
    try:
        connection = mysql.connector.connect(
            host='sql11.freemysqlhosting.net',
            database='sql11692048',
            user='sql11692048',
            password='GdVpfiC7JD',
            port='3306'
        )
        if connection.is_connected():
            print('Connected to MySQL database')
            
            # Execute a test query
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM `zodiac_sign_feedback` LIMIT 1")
            result = cursor.fetchone()
            if result:
                print('Test query executed successfully:', result)
            else:
                print('Test query returned no results')

    except Error as e:
        print(f"Error connecting to MySQL database: {e}")

    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")

if __name__ == "__main__":
    test_database_connection()
