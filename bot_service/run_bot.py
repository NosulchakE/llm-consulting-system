#!/usr/bin/env python
import asyncio
import sys
import os

sys.path.append(os.path.dirname(__file__))

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from app.core.config import settings

# Создаем бота без проверки при старте
bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
dp = Dispatcher()

# Простейший хендлер
@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("✅ Бот работает в демо-режиме!")

@dp.message()
async def echo(message: types.Message):
    await message.answer(f"📝 Вы написали: {message.text}")

async def main():
    if not settings.TELEGRAM_BOT_TOKEN:
        print("❌ Токен не установлен")
        return
    
    print("🤖 Запуск бота (демо-режим, без проверки)...")
    
    # Запускаем polling с игнорированием ошибок подключения
    try:
        await dp.start_polling(bot, skip_updates=True)
    except Exception as e:
        print(f"⚠️ Ошибка подключения, но бот пытается работать: {e}")
        # Продолжаем попытку
        await dp.start_polling(bot, skip_updates=True)

if __name__ == "__main__":
    asyncio.run(main())
