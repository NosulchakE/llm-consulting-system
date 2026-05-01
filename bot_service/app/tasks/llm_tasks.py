from celery import shared_task
import asyncio
from app.services.openrouter_client import call_openrouter
import redis.asyncio as redis
from app.core.config import settings

@shared_task(name="llm_request")
def llm_request(tg_chat_id: int, prompt: str):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    try:
        response = loop.run_until_complete(call_openrouter(prompt))
        loop.run_until_complete(store_result(tg_chat_id, response))
        return response
    finally:
        loop.close()

async def store_result(tg_chat_id: int, response: str):
    redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)
    await redis_client.setex(f"llm_response:{tg_chat_id}", 300, response)
    await redis_client.close()
