import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    """
    Возвращает подключение к базе данных PostgreSQL, используя переменные окружения.
    """
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )
        return conn
    except Exception as e:
        print(f"Ошибка подключения к базе данных: {e}")
        raise

def init_db(conn):
    """
    Инициализирует базу данных: создаёт таблицу logs, если она отсутствует.
    """
    try:
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS logs (
                id SERIAL PRIMARY KEY,
                content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        conn.commit()
        cur.close()
        print("Таблица 'logs' готова для работы.")
    except Exception as e:
        print(f"Ошибка инициализации БД: {e}")
        conn.rollback()
        raise
