# 1. Use base Python image
FROM python:3.10

# 2. Set working directory inside container
WORKDIR /app

# 3. Prevent Python from writing pyc files and buffering stdout
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 4. Install dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# 5. Copy project files into container
COPY . /app/

# 6. Expose port Django runs on
EXPOSE 8000

# 7. Default command to run Django server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
