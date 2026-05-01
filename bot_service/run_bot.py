#!/usr/bin/env python
import asyncio
import sys
import os

sys.path.append(os.path.dirname(__file__))

from app.bot.dispatcher import dp, bot
from app.core.config import settings

async def main():
    if not settings.TELEGRAM_BOT_TOKEN or settings.TELEGRAM_BOT_TOKEN == "your_telegram_bot_token_here":
        print("❌ TELEGRAM_BOT_TOKEN не установлен в .env файле")
        print("Получите токен у @BotFather и добавьте в bot_service/.env")
        return
    
    print("🤖 Запуск Telegram бота...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
