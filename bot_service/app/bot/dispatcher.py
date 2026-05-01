from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from app.core.config import settings
from aiogram.client.default import DefaultBotProperties

bot = Bot(token=settings.TELEGRAM_BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
