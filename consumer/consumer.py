import json
import time
import os
from kafka import KafkaConsumer
from dotenv import load_dotenv
from utils.db import get_db_connection, init_db

# Загрузка переменных окружения
load_dotenv()

KAFKA_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
TOPIC = os.getenv("KAFKA_TOPIC")

def create_consumer():
    """
    Создаёт и возвращает объект KafkaConsumer с десериализацией JSON.
    """
    return KafkaConsumer(
        TOPIC,
        bootstrap_servers=KAFKA_SERVERS,
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        value_deserializer=lambda m: json.loads(m.decode('utf-8'))
    )

if __name__ == "__main__":
    # Инициализируем базу данных (создаем таблицу, если её нет)
    try:
        conn = get_db_connection()
        init_db(conn)
        conn.close()
        print("База данных успешно инициализирована.")
    except Exception as e:
        print(f"Ошибка при инициализации БД: {e}")
        exit(1)

    consumer = create_consumer()
    print("Consumer запущен, ожидаем сообщения из Kafka...")

    for message in consumer:
        log_data = message.value
        print(f"Получено сообщение: {log_data}")
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO logs (content) VALUES (%s)",
                (log_data.get("log"),)
            )
            conn.commit()
            cur.close()
            conn.close()
        except Exception as e:
            print(f"Ошибка при записи в БД: {e}")
        time.sleep(0.2)  # Необязательная задержка
