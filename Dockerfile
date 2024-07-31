# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Add Poetry to PATH
ENV PATH="/root/.local/bin:$PATH"

# Create a directory for the app
WORKDIR /app

# Copy the Poetry configuration files
COPY pyproject.toml poetry.lock* /app/

# Install Python dependencies using Poetry
RUN poetry install --no-root

# Copy the rest of the application code
COPY . /app/

# Define the entry point for the container
CMD ["celery", "-A", "ct_spider_i", "worker", "--loglevel=info"]
