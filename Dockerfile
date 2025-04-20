# Use a standard Python base image
FROM python:3.11-slim

# Copy the requirements file
COPY requirements.txt /tmp/requirements.txt

# Install dependencies globally in the default Python environment
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Optional: Add a command to list installed packages for debugging during build
RUN pip list

# Set the working directory in the container for your application code
WORKDIR /app

# Copy the application code
COPY app.py ./

# Expose the port the Flask app will run on
EXPOSE 5000

# Command to run the application using Gunicorn via python -m
CMD ["python", "-m", "gunicorn", "--bind", "0.0.0.0:5000", "app:app"]