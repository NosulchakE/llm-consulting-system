#!/usr/bin/env python
import asyncio
import sys
import os
import socket
import ssl
import aiohttp

# Отключаем IPv6
socket.setdefaulttimeout(30)

sys.path.append(os.path.dirname(__file__))

from app.bot.dispatcher import dp, bot
from app.core.config import settings

async def main():
    if not settings.TELEGRAM_BOT_TOKEN or settings.TELEGRAM_BOT_TOKEN == "your_telegram_bot_token_here":
        print("❌ TELEGRAM_BOT_TOKEN не установлен")
        return
    
    print("🤖 Запуск Telegram бота...")
    
    try:
        # Проверяем бота
        me = await bot.get_me()
        print(f"✅ Бот запущен: @{me.username}")
        
        # Запускаем polling
        await dp.start_polling(bot)
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    asyncio.run(main())
