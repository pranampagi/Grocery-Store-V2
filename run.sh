#!/bin/bash

# Start Redis
echo "Starting Redis..."
redis-server --daemonize yes
sleep 2

# Start Mailhog
echo "Starting Mailhog..."
nohup mailhog > mailhog.log 2>&1 &

# Start Backend
echo "Starting Backend..."
cd backend
if [ -d ".venv" ]; then
    source .venv/bin/activate
fi
nohup python3 app.py > backend.log 2>&1 &

# Start Celery
echo "Starting Celery Worker and Beat..."
nohup celery -A app.celery_app worker --loglevel INFO > celery_worker.log 2>&1 &
nohup celery -A app.celery_app beat --loglevel INFO > celery_beat.log 2>&1 &

# Start Frontend
echo "Starting Frontend..."
cd ../frontend
nohup npm run serve > frontend.log 2>&1 &

echo "------------------------------------------------"
echo "All services are starting up in the background."
echo "Backend: http://localhost:5000"
echo "Frontend: http://localhost:8080 (or 8081)"
echo "Mailhog: http://localhost:8025"
echo "------------------------------------------------"
echo "Check the *.log files in backend/ and frontend/ for progress."
