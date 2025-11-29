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
RUN pip install --no-cache-dir -r requirements.txt \
 && pip install gunicorn

# Copy the project code
COPY . .
EXPOSE 8002
# Command to run when starting the container
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "churchis.wsgi:application"]
