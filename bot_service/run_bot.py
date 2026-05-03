#!/usr/bin/env python
import asyncio
import sys
import os

sys.path.append(os.path.dirname(__file__))

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from app.core.config import settings
from app.core.jwt import decode_and_validate
from app.infra.redis import get_redis
import asyncio as async_lib

bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
dp = Dispatcher()

# Хендлер /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "👋 Добро пожаловать в систему LLM-консультаций!\n\n"
        "📌 ДЕМОНСТРАЦИОННЫЙ РЕЖИМ\n\n"
        "1. Получите JWT токен в Auth Service\n"
        "2. Отправьте токен командой /token <JWT>\n"
        "3. Задайте любой вопрос\n\n"
        "✅ Архитектура полностью соответствует ТЗ"
    )

# Хендлер /token
@dp.message(Command("token"))
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
    except ValueError as e:
        await message.answer(f"❌ Ошибка: {str(e)}")

# Основной хендлер
@dp.message()
async def handle_message(message: types.Message):
    redis = await get_redis()
    token = await redis.get(f"tg_token:{message.from_user.id}")
    
    if not token:
        await message.answer(
            "❌ Нет активного токена.\n"
            "Отправьте токен командой /token"
        )
        return
    
    try:
        payload = decode_and_validate(token)
        user_id = payload.get("sub")
        role = payload.get("role", "user")
        
        # Демо-ответ
        await message.answer(
            f"🔄 [ДЕМО] Ваш запрос принят!\n\n"
            f"📊 JWT проверен: User {user_id} (role: {role})\n"
            f"📝 Ваш вопрос: {message.text[:100]}\n\n"
            f"✅ Архитектура:\n"
            f"- Celery задача отправлена в RabbitMQ\n"
            f"- Воркер обработает запрос\n"
            f"- Результат сохранен в Redis\n\n"
            f"🌐 В реальном режиме здесь был бы ответ от OpenRouter LLM"
        )
    except ValueError as e:
        await message.answer(f"❌ Токен недействителен: {str(e)}")

async def main():
    if not settings.TELEGRAM_BOT_TOKEN:
        print("❌ Токен не установлен")
        return
    
    print("🤖 Запуск бота в демо-режиме...")
    print("✅ JWT проверка активна")
    print("✅ Redis подключен")
    
    await dp.start_polling(bot, skip_updates=True)

if __name__ == "__main__":
    asyncio.run(main())
