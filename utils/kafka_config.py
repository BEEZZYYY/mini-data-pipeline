import os
from dotenv import load_dotenv

load_dotenv()

# Конфигурационные константы для Kafka
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC")

def get_kafka_config():
    """
    Возвращает словарь с настройками для подключения к Kafka.
    """
    return {
        "bootstrap_servers": KAFKA_BOOTSTRAP_SERVERS,
        "topic": KAFKA_TOPIC
    }
