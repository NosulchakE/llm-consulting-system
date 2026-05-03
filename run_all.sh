#!/bin/bash
echo "Запуск сервисов..."

mkdir -p logs 

export HTTP_PROXY="http://nthtRt:KAyary@45.129.184.86:8000"
export HTTPS_PROXY="http://nthtRt:KAyary@45.129.184.86:8000"

source auth_service/venv/bin/activate
cd auth_service
uvicorn app.main:app --port 8000 > ../logs/auth.log 2>&1 &
cd ..

source bot_service/venv/bin/activate
cd bot_service
uvicorn app.main:app --port 8001 > ../logs/bot_api.log 2>&1 &
python run_bot.py > ../logs/bot.log 2>&1 &
celery -A app.infra.celery_app worker > ../logs/celery.log 2>&1 &
cd ..

echo "Запущено: http://localhost:8000/docs"
