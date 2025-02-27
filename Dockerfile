# Use the official Python image as the base
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the local application files to the container
COPY . .

# Install system dependencies (if needed)
RUN apt-get update && apt-get install -y build-essential libssl-dev

# Install Python dependencies with reduced memory usage
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir --no-build-isolation -r requirements.txt

# Expose the port Streamlit runs on
EXPOSE 8501

# Command to run the app
CMD ["streamlit", "run", "app.py"]
