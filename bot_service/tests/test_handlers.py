import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from aiogram.types import Message, User, Chat
from jose import jwt
from app.core.config import settings
from app.bot.handlers import cmd_start, cmd_token, handle_message


@pytest.fixture
def mock_message():
    msg = AsyncMock(spec=Message)
    msg.from_user = User(id=123, is_bot=False, first_name="Test")
    msg.chat = Chat(id=123, type="private")
    msg.text = ""
    # Настраиваем answer как awaitable
    msg.answer = AsyncMock()
    return msg

@pytest.mark.asyncio
async def test_cmd_start(mock_message):
    await cmd_start(mock_message)
    mock_message.answer.assert_called_once()

@pytest.mark.asyncio
async def test_cmd_token_valid(mock_message):
    token = jwt.encode({"sub": "123", "role": "user"}, settings.JWT_SECRET, algorithm=settings.JWT_ALG)
    mock_message.text = f"/token {token}"
    with patch("app.bot.handlers.get_redis") as mock_redis:
        mock_redis_instance = AsyncMock()
        mock_redis.return_value = mock_redis_instance
        await cmd_token(mock_message)
        mock_redis_instance.setex.assert_called_once()
        mock_message.answer.assert_called_once()

@pytest.mark.asyncio
async def test_cmd_token_invalid(mock_message):
    mock_message.text = "/token invalid_token"
    await cmd_token(mock_message)
    mock_message.answer.assert_called_once()

@pytest.mark.asyncio
async def test_handle_message_no_token(mock_message):
    with patch("app.bot.handlers.get_redis") as mock_redis:
        mock_redis_instance = AsyncMock()
        mock_redis_instance.get = AsyncMock(return_value=None)
        mock_redis.return_value = mock_redis_instance
        await handle_message(mock_message)
        mock_message.answer.assert_called_once()

@pytest.mark.asyncio
async def test_handle_message_with_token(mock_message):
    token = jwt.encode({"sub": "123", "role": "user"}, settings.JWT_SECRET, algorithm=settings.JWT_ALG)
    with patch("app.bot.handlers.get_redis") as mock_redis, \
         patch("app.bot.handlers.llm_request") as mock_llm:
        
        # Настраиваем мок Redis
        mock_redis_instance = AsyncMock()
        mock_redis_instance.get = AsyncMock(return_value=token)
        mock_redis.return_value = mock_redis_instance
        
        # Настраиваем мок llm_request.delay
        mock_llm.delay = MagicMock()
        
        # Вызываем хендлер
        await handle_message(mock_message)
        
        # Проверяем, что delay был вызван один раз с правильными аргументами
        mock_llm.delay.assert_called_once_with(123, "")
        mock_message.answer.assert_called_once()
