FROM python:3.13-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Set environment variables
ENV PORT=8001
ENV HOST=0.0.0.0

# Command to run the application
CMD cd library_api && fastapi dev main.py --port ${PORT} --host ${HOST}
