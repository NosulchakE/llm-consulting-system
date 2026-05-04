# LLM Consulting System

Двухсервисная система LLM-консультаций с JWT аутентификацией.

## Архитектура

| Сервис | Технологии | Функции |
|--------|-----------|---------|
| **Auth Service** | FastAPI, SQLite, JWT | Регистрация, логин, выдача токенов |
| **Bot Service** | aiogram, Celery, Redis | Приём команд, проверка JWT, отправка задач |

**Очереди и хранение:** RabbitMQ (брокер), Redis (кэш/результаты), Celery (воркеры).

## Требования

- Python 3.11+
- Redis
- RabbitMQ
- uv (пакетный менеджер)

## Быстрый старт

```bash
git clone <repo-url>
cd llm-consulting-system
chmod +x *.sh
./setup.sh              # установка зависимостей, Redis, RabbitMQ
./run_all.sh            # запуск всех сервисов
make test               # запуск тестов
```
#### endpoints Auth Service

Метод	Путь	Описание
POST	/api/auth/register	Регистрация (email, password)

POST	/api/auth/login	Логин → JWT

GET	/api/auth/me	Профиль (требуется JWT)

#### Telegram бот

Команды:

/start — приветствие

/token <JWT> — привязать токен к Telegram user_id

Любой текст — вопрос к LLM (через Celery → RabbitMQ → OpenRouter)


Статус реализации

- Auth Service (регистрация, логин, JWT, /me)

- RabbitMQ (очереди, consumers)

- Redis (кэш, хранение токенов)

- Celery (воркер, задачи)

- Telegram бот — не подключён к api.telegram.org (сетевая блокировка на территории РФ)

Тесты
```bash
cd auth_service && pytest -v   # модульные + интеграционные
cd bot_service && pytest -v    # unit-тесты, мокинг Redis/Celery
```
#### Демонстрация (скриншоты)

Swagger Auth Service

Регистрация

Логин → JWT

/auth/me

Redis PONG

Celery worker logs

RabbitMQ queues

Тесты pytest

Ошибка подключения бота



