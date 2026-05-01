#!/bin/bash
echo "🚀 Установка LLM Consulting System..."

# Установка Redis
sudo apt update
sudo apt install -y redis-server
sudo systemctl start redis-server

# Установка RabbitMQ
sudo apt install -y rabbitmq-server
sudo systemctl start rabbitmq-server

# Установка uv
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.cargo/env

# Настройка Auth Service
cd auth_service
python3 -m venv venv
source venv/bin/activate
uv pip install -e .
deactivate
cd ..

# Настройка Bot Service
cd bot_service
python3 -m venv venv
source venv/bin/activate
uv pip install -e .
deactivate
cd ..

echo "✅ Установка завершена!"
