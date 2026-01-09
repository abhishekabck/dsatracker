# Start from a Python base image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 1. Set the working directory
WORKDIR /app

# 2. Copy requirements (Note the change from /code/ to ./)
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# 3. Copy the entire Django project into the current WORKDIR
COPY . .

RUN python manage.py collectstatic --noinput

# 4. Expose the port
EXPOSE 8000

# 5. The startup command
CMD ["sh", "-c", "python manage.py migrate && gunicorn --bind 0.0.0.0:8000 DSATracker.wsgi:application"]