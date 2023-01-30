# Use an official Python runtime as the base image
FROM python:3.8

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Copy the rest of the application files
COPY . .

# Make port 80 available to the world outside this container
EXPOSE 3000

# Run the command to start the application
CMD ["python", "app.py"]