from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiohttp_socks import ProxyConnector
from app.core.config import settings

# Функция для создания бота с прокси
async def create_bot():
    """Создает экземпляр бота с SOCKS5 прокси"""
    PROXY_URL = "socks5://nthtRt:KAyary@45.129.184.86:8000"
    
    connector = ProxyConnector.from_url(PROXY_URL)
    session = AiohttpSession(connector=connector)
    
    return Bot(
        token=settings.TELEGRAM_BOT_TOKEN,
        session=session,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
#  логин и пароль 
# PROXY_URL = "http://nthtRt:KAyary@45.129.184.86:8000"

# Создаем бота позже, при старте
bot = None
dp = Dispatcher()

async def get_bot():
    global bot
    if bot is None:
        bot = await create_bot()
    return bot
