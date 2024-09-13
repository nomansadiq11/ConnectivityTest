# Use the official Python image from Docker Hub
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Create a new sources.list and use an alternative Debian mirror
RUN echo "deb http://ftp.us.debian.org/debian stable main contrib non-free" > /etc/apt/sources.list && \
    apt-get clean && \
    apt-get update --fix-missing && \
    apt-get install -y \
    dnsutils \
    curl \
    netcat-openbsd \
    inetutils-ping \
    --fix-missing && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy the requirements.txt file (if you have one)
COPY requirements.txt .

# Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY ./app .

# Expose the port that the Flask app runs on
EXPOSE 5000

# Command to run the application
CMD ["python", "app.py"]
