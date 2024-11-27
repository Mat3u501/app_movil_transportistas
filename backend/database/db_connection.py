import pymysql

def get_db_connection():
    """
    Establish a connection to the MySQL database.
    :return: pymysql Connection object or None if failed.
    """
    try:
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='',
            database='transportistas_app',
            port=3306,
            cursorclass=pymysql.cursors.DictCursor
        )
        return connection
    except pymysql.MySQLError as e:
        print(f"Error connecting to database: {e}")
        return None

def close_connection(connection):
    """
    Safely close the database connection.
    :param connection: pymysql Connection object.
    """
    if connection and connection.open:
        connection.close()
