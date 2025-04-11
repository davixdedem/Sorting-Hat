# Start from a lightweight ARM-compatible base
FROM arm64v8/python:3.11.2-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libffi-dev \
    libssl-dev \
    libbz2-dev \
    libreadline-dev \
    libsqlite3-dev \
    libncursesw5-dev \
    libgdbm-dev \
    liblzma-dev \
    zlib1g-dev \
    curl \
    wget \
    git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# (Optional) If not using the base image with Python 3.11.2,
# you can build from source instead. Uncomment below if needed.
#RUN wget https://www.python.org/ftp/python/3.11.2/Python-3.11.2.tgz && \
#    tar -xvzf Python-3.11.2.tgz && \
#    cd Python-3.11.2 && \
#    ./configure --enable-optimizations && \
#    make -j$(nproc) && \
#    make altinstall && \
#    cd .. && rm -rf Python-3.11.2 Python-3.11.2.tgz

# Install Python dependencies
RUN pip install --upgrade pip \
    && pip install -r requirements.txt
