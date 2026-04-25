FROM python:3.12-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Install Playwright
RUN playwright install chromium

# Copy application code
COPY src/ ./src/
COPY config/ ./config/

# Copy main entry point
COPY main.py .

# Create output directory
RUN mkdir -p output

# Make script executable
RUN chmod +x main.py

CMD ["python3", "main.py"]