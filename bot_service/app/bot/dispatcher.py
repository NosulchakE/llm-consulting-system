from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiohttp_socks import ProxyConnector
from app.core.config import settings

#  логин и пароль 
PROXY_URL = "http://nthtRt:KAyary@45.129.184.86:8000"

connector = ProxyConnector.from_url(PROXY_URL)
session = AiohttpSession(connector=connector)

bot = Bot(
    token=settings.TELEGRAM_BOT_TOKEN,
    session=session,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

dp = Dispatcher()
