import mysql.connector
import config

connection = mysql.connector.connect(
    host=config.DB_HOST,
    user=config.DB_USER,
    password=config.DB_PASSWORD,
    database=config.DB_NAME
)

cursor = connection.cursor(dictionary=True)


def execute(query, params=None):
    cursor.execute(query, params or ())
    connection.commit()
    return cursor


def fetchone(query, params=None):
    cursor.execute(query, params or ())
    return cursor.fetchone()


def fetchall(query, params=None):
    cursor.execute(query, params or ())
    return cursor.fetchall()