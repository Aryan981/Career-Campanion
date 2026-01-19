#!/bin/bash

# Function to kill background processes on exit
cleanup() {
    echo "Shutting down..."
    kill $(jobs -p)
    exit
}

trap cleanup SIGINT SIGTERM

echo "Starting AI Career Companion..."

# 1. Start Backend
echo "Starting Backend on http://localhost:8000..."
export PYTHONPATH=$PYTHONPATH:$(pwd)
python3 backend/main.py &
BACKEND_PID=$!
# No need to cd backend

# 2. Start Frontend
echo "Starting Frontend on http://localhost:3000..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo "Application is running!"
echo "Press Ctrl+C to stop."

# Wait for both processes
wait $BACKEND_PID $FRONTEND_PID
