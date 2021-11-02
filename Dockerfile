# syntax=docker/dockerfile:1

# The docker image being used.
FROM python:3

# Working directory in docker container.
WORKDIR /usr/src/app

# Copies requirements from repo to container working directory.
COPY requirements.txt ./

# Download requirements to container
RUN pip install --no-cache-dir -r requirements.txt

# Copy other files to working directory
COPY . .

CMD ["python", "./PacMan/src/pacman.py"]
