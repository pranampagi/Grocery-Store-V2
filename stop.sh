#!/bin/bash

echo "Stopping all Grocery Store services..."

# Kill Frontend (vue-cli-service)
echo "Stopping Frontend..."
pkill -f "vue-cli-service"

# Kill Backend and Celery (Python processes)
echo "Stopping Backend and Celery..."
pkill -f "python3 app.py"
pkill -f "celery -A app.celery_app"

# Kill Mailhog
echo "Stopping Mailhog..."
pkill -f "mailhog"

# Kill Redis
echo "Stopping Redis..."
redis-cli shutdown 2>/dev/null || pkill -f "redis-server"

echo "------------------------------------------------"
echo "All services stopped."
echo "------------------------------------------------"
