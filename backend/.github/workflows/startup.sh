FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=churchis.settings

# Set the working directory
WORKDIR /app

# Install system dependencies - only what's needed
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy and install requirements first (better caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project code
COPY . .

# Create a directory for static files
RUN mkdir -p /app/staticfiles

# Add startup script and make it executable
COPY startup.sh /app/
RUN chmod +x /app/startup.sh

# Expose the port
EXPOSE 8000

# Command to run the application
CMD ["startup.sh"]