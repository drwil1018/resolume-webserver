#!/bin/zsh

# Configuration
BACKEND_PORT=5002  # Changed from 5000 to avoid conflict with AirPlay
FRONTEND_PORT=3000

# Get the local IP address
LOCAL_IP=$(ifconfig | grep "inet " | grep -v 127.0.0.1 | awk '{print $2}' | head -n 1)

echo "========================================================"
echo "Local Network Setup Information"
echo "========================================================"
echo "Your local IP address: $LOCAL_IP"
echo ""
echo "Frontend will be available at: http://$LOCAL_IP:$FRONTEND_PORT"
echo "Backend API will be available at: http://$LOCAL_IP:$BACKEND_PORT"
echo ""
echo "To access from other devices on your network:"
echo "1. Make sure they're connected to the same WiFi/network"
echo "2. Have them visit http://$LOCAL_IP:$FRONTEND_PORT in their browser"
echo "========================================================"

# Create an updated .env file with the local IP for backend API
echo "VITE_API_URL=http://$LOCAL_IP:$BACKEND_PORT" > ./frontend/.env

# Start backend server
echo "Starting backend server..."
cd backend

# Check if virtual environment exists
if [ -d ".venv" ]; then
    echo "Activating virtual environment..."
    source .venv/bin/activate
    
    # Check if the activation was successful
    if [ $? -ne 0 ]; then
        echo "Error: Failed to activate virtual environment"
        exit 1
    fi
else
    echo "Error: Virtual environment not found. Please create it with:"
    echo "cd backend && python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

# Set port as environment variable
export PORT=$BACKEND_PORT

# Start the Flask app
python3 app.py &
BACKEND_PID=$!

# Check if backend started successfully
sleep 2
if ! ps -p $BACKEND_PID > /dev/null; then
    echo "Error: Failed to start backend server"
    exit 1
fi

cd ../frontend
echo "Starting frontend server..."
export FRONTEND_PORT=$FRONTEND_PORT
npm run dev

# Cleanup when terminated
kill $BACKEND_PID 2>/dev/null
