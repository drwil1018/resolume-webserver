# Use Python 3.9 as the base image
FROM python:3.9-slim

# Set working directory in the container
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Create the uploads directory if it doesn't exist
RUN mkdir -p resolume_uploads

# Expose port 5001 (the port we're using for the backend)
EXPOSE 5001

# Environment variable for Flask
ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV PORT=5001

# Command to run the application
CMD ["python", "app.py"]
