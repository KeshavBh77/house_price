# Use slim Python image
FROM python:3.10-slim

WORKDIR /app

# Copy only requirements first to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy rest of the app code
COPY . .

# Expose the app port
EXPOSE 5001

# Run the app
CMD ["python", "app.py"]