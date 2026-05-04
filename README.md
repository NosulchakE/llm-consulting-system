# LLM Consulting System

Двухсервисная система LLM-консультаций с JWT аутентификацией.

## Архитектура
- **Auth Service** (FastAPI) - регистрация, логин, JWT токены
- **Bot Service** (aiogram) - Telegram бот с проверкой JWT
- **Celery + RabbitMQ** - асинхронная обработка LLM запросов
- **Redis** - хранение токенов и результатов
- **OpenRouter** - LLM провайдер

## Быстрый старт

