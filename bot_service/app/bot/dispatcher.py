from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiohttp import ClientTimeout, TCPConnector
from app.core.config import settings

def get_bot():
    """Фабрика для создания бота (чтобы избежать проблем с event loop)"""
    timeout = ClientTimeout(total=60, connect=30)
    connector = TCPConnector(
        ttl_dns_cache=300,
        use_dns_cache=True,
        limit=10,
        family=2  # IPv4
    )
    session = AiohttpSession(timeout=timeout, connector=connector)
    
    return Bot(
        token=settings.TELEGRAM_BOT_TOKEN,
        session=session,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

# Создаем бота лениво (при первом использовании)
bot = None
dp = Dispatcher()

def get_bot_instance():
    global bot
    if bot is None:
        bot = get_bot()
    return bot
