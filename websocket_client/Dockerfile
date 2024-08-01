FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy only the requirements file first to leverage Docker's cache
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code and the wait_db.sh script
COPY . /app

CMD ["sh", "-c", "python3 client_websocket.py"]