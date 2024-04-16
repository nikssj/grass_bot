# Use the official Python image as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the Python script into the container at /app
COPY bot.py ./
COPY pags.csv ./

# Install necessary tools
RUN apt-get update && apt-get install -y wget gnupg2 unzip \
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable

# Download and install ChromeDriver
RUN wget https://chromedriver.storage.googleapis.com/98.0.4758.102/chromedriver_linux64.zip \
    && unzip chromedriver_linux64.zip -d /usr/bin/ \
    && rm chromedriver_linux64.zip \
    && apt-get clean

# Install Selenium
RUN pip install selenium

# Command to run on container start
CMD ["python", "./bot.py"]
