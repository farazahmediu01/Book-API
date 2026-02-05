# From Command - Specifies the base image to use for the Docker container
# Using slim version of Python 3.12 for a smaller image size
# Docker find this file at local first before pulling from docker hub.
FROM python:3.12-slim 


# 1. Set the working directory inside the container to /app. This is where all
#    subsequent commands will be executed and where the application code will reside.
WORKDIR /app

# Install uv
# --no-cache-dir to reduce image size by not caching the installation files
RUN pip install --no-cache-dir uv 

# # Copy only dependency files first (better Docker cache)
# source(pyproject.toml uv.lock) -> destination(./) in the container
# the reson to add uv.lock file is to also not to create anthor lock file in the container, and to make sure the exact versions of dependencies are installed as specified in the lock file.   
COPY pyproject.toml uv.lock ./

# Install dependencies (uses uv.lock for exact versions)
# --frozen to ensure the lock file is strictly followed
# --no-dev to skip development dependencies
RUN uv sync --frozen --no-dev

# Copy application code last again from source(.) to destination(.) in the container. 
# This allows Docker to cache the dependency installation step and only re-run it if the dependency files change.
#  Improving build times during development.
COPY . .

EXPOSE 8000


# Metadata about the image
LABEL NAME="FastAPI Application" \
      VERSION="1.0" \
      DESCRIPTION="A FastAPI application running in a Docker container" \
      AUTHOR="Faraz Ahmed"

CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4 "]

