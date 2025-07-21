# Use an official Python base image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy only the requirements first (for caching install layers)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code
COPY . .

# Run the FastAPI app using uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
