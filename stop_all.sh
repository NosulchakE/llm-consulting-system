#!/bin/bash
pkill -f "uvicorn app.main:app"
pkill -f "run_bot.py"
pkill -f "celery"
echo "Сервисы остановлены"
