import pytest
import respx
from httpx import Response
from app.services.openrouter_client import call_openrouter

@pytest.mark.asyncio
async def test_call_openrouter_success():
    mock_response = {
        "choices": [{"message": {"content": "Привет, это тестовый ответ!"}}]
    }
    with respx.mock:
        respx.post("https://openrouter.ai/api/v1/chat/completions").mock(
            return_value=Response(200, json=mock_response)
        )
        result = await call_openrouter("Тестовый запрос")
        assert result == "Привет, это тестовый ответ!"
        assert respx.calls.call_count == 1

@pytest.mark.asyncio
async def test_call_openrouter_timeout():
    with respx.mock:
        respx.post("https://openrouter.ai/api/v1/chat/completions").mock(
            side_effect=TimeoutError()
        )
        result = await call_openrouter("Test")
        assert "слишком много времени" in result
