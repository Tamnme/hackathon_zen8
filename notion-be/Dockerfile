FROM python:3.11-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=run.py

# Create database tables
RUN python3 -c "from app import create_app; from app.models import db; app = create_app(); app.app_context().push(); db.create_all()"

# Expose the port the app runs on
EXPOSE 8080

# Command to run the application
CMD ["python3", "run.py"] 