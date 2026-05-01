from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiohttp import ClientTimeout, TCPConnector
from app.core.config import settings

# Настройки для обхода проблем с сетью
timeout = ClientTimeout(total=60, connect=30)
connector = TCPConnector(
    ttl_dns_cache=300,
    use_dns_cache=True,
    limit=10,
    family=2  # Принудительно IPv4
)

session = AiohttpSession(
    timeout=timeout,
    connector=connector
)

bot = Bot(
    token=settings.TELEGRAM_BOT_TOKEN,
    session=session,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

dp = Dispatcher()
