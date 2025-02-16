# Use Python 3.9 as base image
FROM python:3.9

# Set the working directory inside the container
WORKDIR /app

# Copy everything from the host machine to the container
COPY . /app /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Start the FastAPI app using Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
