# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /bangkit_ML

# Copy the current directory contents into the container at /app
COPY . /bangkit_ML

# Install the required Python dependencies
RUN pip install fastapi uvicorn scikit-learn pandas

# Make port 8000 available to the world outside the container
EXPOSE 8000

# Define environment variables
ENV PYTHONUNBUFFERED=1

# Run the application using uvicorn when the container starts
CMD ["uvicorn", "ml_api:app", "--host", "0.0.0.0", "--port", "8000"]
