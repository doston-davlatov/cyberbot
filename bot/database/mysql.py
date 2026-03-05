# bot/database/mysql.py
import mysql.connector
from mysql.connector import pooling
import logging
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

logger = logging.getLogger(__name__)

connection_pool = pooling.MySQLConnectionPool(
    pool_name="mypool",
    pool_size=5,
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_NAME
)

def execute_query(query: str, params: tuple = ()):
    conn = None
    try:
        conn = connection_pool.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
    except mysql.connector.Error as e:
        logger.error(f"DB query xato: {e}")
    finally:
        if conn:
            conn.close()

def fetch_one(query: str, params: tuple = ()):
    conn = None
    try:
        conn = connection_pool.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, params)
        return cursor.fetchone()
    except mysql.connector.Error as e:
        logger.error(f"DB fetch xato: {e}")
        return None
    finally:
        if conn:
            conn.close()