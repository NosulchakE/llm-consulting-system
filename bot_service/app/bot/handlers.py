import logging
from aiogram import Router, types
from aiogram.filters import Command

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    logger.info(f"Start от {message.from_user.id}")
    await message.answer("👋 Бот работает! Отправь /token")

@router.message(Command("token"))
async def cmd_token(message: types.Message):
    logger.info(f"Token от {message.from_user.id}")
    await message.answer("✅ Токен принят (пока заглушка)")

@router.message()
async def handle_message(message: types.Message):
    logger.info(f"Сообщение от {message.from_user.id}: {message.text[:50]}")
    await message.answer(f"Получено: {message.text[:100]}")
