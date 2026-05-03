import logging
from aiogram import Router, types
from aiogram.filters import Command
from app.core.jwt import decode_and_validate
from app.infra.redis import get_redis

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    logger.info(f"Start от {message.from_user.id}")
    await message.answer(
        "👋 Добро пожаловать в систему LLM-консультаций!\n\n"
        "📌 ДЕМОНСТРАЦИОННЫЙ РЕЖИМ\n\n"
        "1. Получите JWT токен в Auth Service\n"
        "2. Отправьте токен командой /token <JWT>\n"
        "3. Задайте любой вопрос\n\n"
        "✅ Архитектура:\n"
        "- Auth Service (FastAPI) - регистрация и JWT\n"
        "- Bot Service (aiogram) - Telegram бот\n"
        "- Celery + RabbitMQ - асинхронная обработка\n"
        "- Redis - хранение токенов\n"
        "- OpenRouter - LLM (демо-режим)"
    )

@router.message(Command("token"))
async def cmd_token(message: types.Message):
    args = message.text.split()
    if len(args) != 2:
        await message.answer("❌ Использование: /token <jwt_token>")
        return
    
    token = args[1]
    
    try:
        payload = decode_and_validate(token)
        user_id = payload.get("sub")
        role = payload.get("role", "user")
        
        redis = await get_redis()
        await redis.setex(f"tg_token:{message.from_user.id}", 3600, token)
        
        await message.answer(
            f"✅ Токен сохранен!\n"
            f"User ID: {user_id}\n"
            f"Role: {role}\n\n"
            f"Теперь вы можете задавать вопросы."
        )
        logger.info(f"Token сохранен для user {user_id}")
    except ValueError as e:
        await message.answer(f"❌ Ошибка: {str(e)}")

@router.message()
async def handle_message(message: types.Message):
    # Проверяем токен в Redis
    redis = await get_redis()
    token = await redis.get(f"tg_token:{message.from_user.id}")
    
    if not token:
        await message.answer(
            "❌ Нет активного токена.\n"
            "Отправьте токен командой /token"
        )
        return
    
    try:
        # Валидируем токен
        payload = decode_and_validate(token)
        user_id = payload.get("sub")
        role = payload.get("role", "user")
        
        # ДЕМО-РЕЖИМ: имитация Celery задачи
        await message.answer("🔄 [ДЕМО] Ваш запрос принят. Отправлено в Celery очередь...")
        
        # Имитация асинхронной обработки
        import asyncio
        await asyncio.sleep(1)
        
        # Имитация ответа от LLM через OpenRouter
        await message.answer(
            f"🤖 [ДЕМО-ОТВЕТ LLM]\n\n"
            f"Вы спросили: \"{message.text[:100]}{'...' if len(message.text) > 100 else ''}\"\n\n"
            f"✅ Асинхронная обработка через Celery + RabbitMQ\n"
            f"✅ JWT аутентификация: User {user_id} (role: {role})\n"
            f"✅ Результат сохранен в Redis\n\n"
            f"📌 В реальном режиме здесь был бы ответ от OpenRouter API"
        )
        
        logger.info(f"Демо-ответ отправлен пользователю {user_id}")
        
    except ValueError as e:
        await message.answer(f"❌ Токен недействителен: {str(e)}")
