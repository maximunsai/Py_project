#Install docker on linux (ubuntu)--------------------
sudo apt-get update
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh ./get-docker.sh --dry-run


#Docker File ----------------------------
# Use the official Python image from the Docker Hub
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip3 install  -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Command to run the application
CMD ["python3", "app.py"]



