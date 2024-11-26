# backend/Dockerfile
FROM public.ecr.aws/docker/library/python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt ./
RUN pip install -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose port 5000 and start the server
EXPOSE 5000
CMD ["python", "app.py"]
