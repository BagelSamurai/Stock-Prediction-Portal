# --- Stage 1: Build Stage ---
# Use a full Python image to install dependencies
FROM python:3.11-slim as builder

WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies required for some Python packages
RUN apt-get update && apt-get install -y --no-install-recommends build-essential

# Install Python dependencies
COPY requirements.txt .
RUN pip wheel --no-cache-dir --wheel-dir /app/wheels -r requirements.txt


# Use a slim Python image for the final application
FROM python:3.11-slim

WORKDIR /app

# Create a non-root user for security
RUN addgroup --system app && adduser --system --group app

# Copy pre-built wheels from the builder stage
COPY --from=builder /app/wheels /wheels

# Install dependencies from wheels
COPY requirements.txt .
RUN pip install --no-cache /wheels/*

# Copy the application code
COPY . .

# Change ownership of the app directory to the non-root user
RUN chown -R app:app /app

# Switch to the non-root user
USER app

# Expose the port Gunicorn will run on
EXPOSE 8000

# Run the application using Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "stock_prediction_main.wsgi"]