# Use a slim, official Python image — small footprint, fewer surprises.
FROM python:3.11-slim

# Don't write .pyc files & unbuffered stdout (logs appear immediately).
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# All work happens inside /app.
WORKDIR /app

# Install dependencies first so Docker can cache this layer.
# If requirements.txt doesn't change, Docker reuses the cache.
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy the application code.
COPY app ./app

# The app listens on this port inside the container.
EXPOSE 8000

# Start the FastAPI app with uvicorn, bound to all interfaces
# so the host machine can reach it through the published port.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]