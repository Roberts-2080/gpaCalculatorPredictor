import mysql.connector
from config.db_config import password


def get_db_connection():
    connection = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password=password,
        database='gpa'
    )
    return connection
