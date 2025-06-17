#!/bin/bash

# Script to build and deploy Docker containers for Resolume Web Server

# Print header
echo "=========================================================="
echo "Resolume Web Server Docker Deployment"
echo "=========================================================="
echo

# Function to check if Docker is installed
check_docker() {
  if ! command -v docker &> /dev/null; then
    echo "Error: Docker is not installed or not in your PATH"
    echo "Please install Docker from https://docs.docker.com/get-docker/"
    exit 1
  fi
  
  if ! command -v docker-compose &> /dev/null; then
    echo "Error: docker-compose is not installed or not in your PATH"
    echo "Please install docker-compose from https://docs.docker.com/compose/install/"
    exit 1
  fi
}

# Function to prepare environment
prepare_env() {
  echo "Preparing environment..."
  
  # Make sure the uploads folder exists
  mkdir -p backend/resolume_uploads
  
  # Copy the .env.docker to .env for the build
  cp frontend/.env.docker frontend/.env
  
  echo "Environment prepared."
  echo
}

# Function to build containers
build_containers() {
  echo "Building Docker containers (this may take a few minutes)..."
  docker-compose build
  
  if [ $? -ne 0 ]; then
    echo "Error: Failed to build Docker containers"
    exit 1
  fi
  
  echo "Containers built successfully."
  echo
}

# Function to start containers
start_containers() {
  echo "Starting containers..."
  docker-compose up -d
  
  if [ $? -ne 0 ]; then
    echo "Error: Failed to start Docker containers"
    exit 1
  fi
  
  echo "Containers started successfully."
  echo
}

# Function to show container status
show_status() {
  echo "Container status:"
  docker-compose ps
  echo
  
  # Get server IP address
  IP_ADDRESS=$(hostname -I | awk '{print $1}')
  
  echo "=========================================================="
  echo "Your Resolume Web Server should now be running!"
  echo
  echo "Access it from this machine at: http://localhost"
  echo "Access from other devices using: http://$IP_ADDRESS"
  echo "=========================================================="
}

# Function to clean up unused resources
cleanup() {
  echo "Cleaning up unused Docker resources..."
  docker system prune -f
  echo "Cleanup complete."
  echo
}

# Main execution
check_docker
prepare_env
build_containers
start_containers
show_status
cleanup

echo "Deployment completed!"
