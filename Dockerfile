# Use an official Python runtime as a parent image
FROM python:3.11

# Set environment variables for Django
ENV DJANGO_SETTINGS_MODULE=receiptprocessor.settings
ENV PYTHONUNBUFFERED 1

# Create and set the working directory
RUN mkdir /app
WORKDIR /app

# Copy the entire Django project folder into the image
COPY ./ /app/

# Copy the Pipfile and Pipfile.lock into the image
COPY Pipfile Pipfile.lock /app/

# Install pipenv (if needed) and Python dependencies
RUN pip install pipenv && pipenv install --deploy --ignore-pipfile

# Expose the port that the application will run on (adjust as needed)
EXPOSE 8000

# Define the command to run your Django application
CMD ["pipenv", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
