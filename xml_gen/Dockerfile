# Start with a base image
FROM python:alpine

# Install dependencies
RUN apk add --no-cache python3 py3-pip

COPY requirements.txt .
# Install your required packages
RUN pip install -r requirements.txt

# Copy your script into the container
COPY . /app/ 

# Expose a port for the API
EXPOSE 8001

# Set the working directory
WORKDIR /app

# Command to run the FastAPI application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
