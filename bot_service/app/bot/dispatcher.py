from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiohttp_socks import ProxyConnector
from app.core.config import settings


#  логин и пароль 
PROXY_URL = "http://nthtRt:KAyary@45.129.184.86:8000"

# Функция для создания бота
async def create_bot():
    connector = ProxyConnector.from_url(PROXY_URL)
    session = AiohttpSession(connector=connector)
    
    return Bot(
        token=settings.TELEGRAM_BOT_TOKEN,
        session=session,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

# Ленивая инициализация
_bot = None

async def get_bot():
    global _bot
    if _bot is None:
        _bot = await create_bot()
    return _bot

dp = Dispatcher()
