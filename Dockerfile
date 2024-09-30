# Use an official Python runtime as a base image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Django project into the container
COPY . .

# Expose port 8000 to allow access to the Django development server
EXPOSE 8001

# Run a management command, e.g., migrate, before starting the Django server
CMD ["sh", "-c", "python manage.py makemigrations && python manage.py migrate && python manage.py create_database && python manage.py runserver 0.0.0.0:8000"]
