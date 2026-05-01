from aiogram import Router, types, F
from aiogram.filters import Command
import asyncio
from app.core.jwt import decode_and_validate
from app.infra.redis import get_redis
from app.tasks.llm_tasks import llm_request

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "👋 Добро пожаловать!\n\n"
        "Для использования бота:\n"
        "1. Зарегистрируйтесь в Auth Service: http://localhost:8000/docs\n"
        "2. Получите JWT токен через POST /auth/login\n"
        "3. Отправьте токен командой /token <jwt_token>\n\n"
        "После этого задавайте любые вопросы!"
    )

@router.message(Command("token"))
async def cmd_token(message: types.Message):
    args = message.text.split()
    if len(args) != 2:
        await message.answer("❌ Использование: /token <jwt_token>")
        return
    
    token = args[1]
    
    try:
        payload = decode_and_validate(token)
        user_id = payload.get("sub")
        role = payload.get("role", "user")
        
        redis = await get_redis()
        await redis.setex(f"tg_token:{message.from_user.id}", 3600, token)
        
        await message.answer(
            f"✅ Токен сохранен!\n"
            f"User ID: {user_id}\n"
            f"Role: {role}\n\n"
            f"Теперь задавайте вопросы."
        )
    except ValueError as e:
        await message.answer(f"❌ Ошибка: {str(e)}")

@router.message(F.text)
async def handle_message(message: types.Message):
    redis = await get_redis()
    token = await redis.get(f"tg_token:{message.from_user.id}")
    
    if not token:
        await message.answer(
            "❌ Нет активного токена.\n"
            "Отправьте токен командой /token"
        )
        return
    
    try:
        decode_and_validate(token)
        await message.answer("🔄 Запрос принят, обрабатываю...")
        
        llm_request.delay(message.from_user.id, message.text)
        
        # Ждем результат
        for _ in range(30):
            await asyncio.sleep(2)
            result = await redis.get(f"llm_response:{message.from_user.id}")
            if result:
                await message.answer(result)
                await redis.delete(f"llm_response:{message.from_user.id}")
                return
        
        await message.answer("⏰ Превышено время ожидания")
    except ValueError as e:
        await message.answer(f"❌ Токен недействителен: {str(e)}")
