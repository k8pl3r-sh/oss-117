FROM python:3.9-slim
# Set the working directory
WORKDIR /app

RUN apt update && apt install -y build-essential libsystemd-dev
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app

# Expose the port the app runs on
EXPOSE 8100

# Command to run Gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8100", "--timeout", "240", "app:app"]
