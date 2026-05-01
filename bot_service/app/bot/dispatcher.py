from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiohttp import ClientTimeout
from app.core.config import settings

def get_bot():
    """Фабрика для создания бота"""
    # Настройки таймаутов
    timeout = ClientTimeout(total=60, connect=30)
    
    # Создаем сессию (без connector параметра)
    session = AiohttpSession(timeout=timeout)
    
    return Bot(
        token=settings.TELEGRAM_BOT_TOKEN,
        session=session,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

# Ленивая инициализация бота
_bot = None

def get_bot_instance():
    global _bot
    if _bot is None:
        _bot = get_bot()
    return _bot

dp = Dispatcher()
