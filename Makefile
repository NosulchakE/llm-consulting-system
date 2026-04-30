# Makefile
.PHONY: setup run stop test clean

setup:
	chmod +x *.sh
	./setup.sh

run:
	./run_all.sh

stop:
	./stop_all.sh

test:
	cd auth_service && source venv/bin/activate && pytest tests/ -v
	cd bot_service && source venv/bin/activate && pytest tests/ -v

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	rm -rf logs/*.log logs/*.pid
	@echo "Очистка завершена"

status:
	@echo "Статус сервисов:"
	@pgrep -f "uvicorn.*8000" > /dev/null && echo "✅ Auth Service: RUNNING" || echo "❌ Auth Service: STOPPED"
	@pgrep -f "uvicorn.*8001" > /dev/null && echo "✅ Bot API: RUNNING" || echo "❌ Bot API: STOPPED"
	@pgrep -f "run_bot.py" > /dev/null && echo "✅ Telegram Bot: RUNNING" || echo "❌ Telegram Bot: STOPPED"
	@pgrep -f "celery" > /dev/null && echo "✅ Celery Worker: RUNNING" || echo "❌ Celery Worker: STOPPED"
