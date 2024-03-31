# api/Dockerfile

# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Install any needed packages specified in requirements.txt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . .

# Make port 5100 available to the world outside this container
EXPOSE 5100

# Define environment variable to ensure Python modules are found
ENV PYTHONPATH /app

# Run app.py when the container launches
CMD ["python", "app.py"]
