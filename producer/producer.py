import time
import json
import random
import os
from kafka import KafkaProducer
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

KAFKA_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
TOPIC = os.getenv("KAFKA_TOPIC")

def create_producer():
    """
    Создаёт и возвращает объект KafkaProducer с сериализацией JSON.
    """
    return KafkaProducer(
        bootstrap_servers=KAFKA_SERVERS,
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

def stream_logs(file_path):
    """
    Генератор, который читает файл построчно и возвращает словарь с логом.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                stripped_line = line.strip()
                if stripped_line:
                    yield {"log": stripped_line}
    except FileNotFoundError:
        print(f"Файл {file_path} не найден.")
        return

if __name__ == "__main__":
    producer = create_producer()
    log_file = os.path.join(os.path.dirname(__file__), '..', 'logs.txt')  # путь к файлу с логами

    print("Начало отправки логов в Kafka...")
    for log_entry in stream_logs(log_file):
        producer.send(TOPIC, value=log_entry)
        print(f"Отправлено: {log_entry}")
        # Задержка для имитации реального времени
        time.sleep(random.uniform(0.5, 1.5))
    producer.flush()
    print("Отправка логов завершена.")
