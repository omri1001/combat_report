# Use Python 3.12 slim image
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /code

# Copy requirements.txt into the container
COPY requirements.txt .

# Install system dependencies and Python dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get purge -y --auto-remove gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy the entire project into the container
COPY . .

# Expose the port (if your application listens on a port)
EXPOSE 8443

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Define the command to run the bot
CMD ["python", "-m", "app.controllers.telegram_bot"]
