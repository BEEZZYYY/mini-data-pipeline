# Mini Data Pipeline

Проект демонстрирует простейший data pipeline с использованием Apache Kafka, PostgreSQL и FastAPI.

## Структура проекта

- **.env**: Файл с переменными окружения.
- **docker-compose.yml**: Конфигурация Docker для Kafka, Zookeeper и PostgreSQL.
- **requirements.txt**: Зависимости Python.
- **logs.txt**: Исходные логи.
- **producer/**: Компонент для отправки логов в Kafka.
- **consumer/**: Компонент для чтения логов из Kafka и записи в БД.
- **api/**: API-сервер для предоставления аналитики.
- **utils/**: Вспомогательные модули (работа с БД и Kafka).

## Запуск

1. Поднимите инфраструктуру:
   ```bash
   docker-compose up -d
