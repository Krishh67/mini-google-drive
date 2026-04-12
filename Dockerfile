# Use lightweight base image
FROM python:3.9-slim

# Set working directory inside the container
WORKDIR /app

# Copy the requirements file first to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project files
COPY . .

# Ensure the uploads directory exists (it's also handled in app.py)
RUN mkdir -p uploads

# Expose port 5000
EXPOSE 5000

# Use gunicorn to run the application
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
