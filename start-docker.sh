#!/bin/bash

# Simple script to start existing Docker containers for Resolume Web Server

echo "Starting Resolume Web Server Docker containers..."
cd "$(dirname "$0")"

# Check if containers exist
if [ "$(docker ps -a -q -f name=resolume-backend)" ]; then
    echo "Starting existing containers..."
    docker-compose up -d
    
    echo "Containers started successfully!"
    echo "- Frontend: http://localhost (port 80)"
    echo "- Backend API: http://localhost:5001"
else
    echo "Containers not found. Please run deploy-docker.sh first to set up the containers."
    echo "Command: ./deploy-docker.sh"
fi
