# LLM Consulting System

Двухсервисная система LLM-консультаций с JWT аутентификацией.

## Архитектура
- **Auth Service** (FastAPI) - регистрация, логин, JWT токены
- **Bot Service** (aiogram) - Telegram бот с проверкой JWT
- **Celery + RabbitMQ** - асинхронная обработка LLM запросов
- **Redis** - хранение токенов и результатов
- **OpenRouter** - LLM провайдер

## Быстрый старт

```bash
git clone https://github.com/YOUR_USERNAME/llm-consulting-system.git
cd llm-consulting-system
chmod +x *.sh
./setup.sh
# Отредактируйте bot_service/.env (добавьте TELEGRAM_BOT_TOKEN и OPENROUTER_API_KEY)
./run_all.sh

Проверка работы
Auth Service Swagger: http://localhost:8000/docs

RabbitMQ Management: http://localhost:15672 (guest/guest)
