# Use Python 3.12 as the base image
FROM python:3.12

# Set environment variables to non-interactive for apt-get
ENV DEBIAN_FRONTEND=noninteractive

# Define your environment variables here
ENV FLASK_APP=main.py \
    FLASK_ENV=development \
    DB_HOST=localhost \
    DB_USER=root \
    DB_PASSWORD=new_password \
    DB_NAME=starmeter \
    DATABASE_URL='mysql://admin:zip.code123%21@test-db.c3u680mys7w2.us-east-1.rds.amazonaws.com:3306/starmeter' \
    SECRET_KEY="baconandeggs"

# Update and install necessary system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    libssl-dev \
    libffi-dev \
    openssl \
    default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

# Additional steps derived from image history
RUN apt-get update && \
    apt-get install -y wget && \
    wget -O get-pip.py https://bootstrap.pypa.io/get-pip.py && \
    python get-pip.py && \
    rm get-pip.py && \
    pip install --upgrade pip==24.2 setuptools==67.0.0 wheel

# Set working directory
WORKDIR /app

# Copy the local code to the container
COPY . /app

# Install required Python packages with updated eventlet and additional packages
RUN python -m pip install --upgrade pip 'setuptools>=67' wheel
RUN python -m pip install --no-cache-dir numpy==1.26.4
RUN python -m pip install Flask==2.2.5 Flask-SocketIO==5.3.4 python-socketio==5.5.2
RUN python -m pip install --prefer-binary pandas==2.0.0
RUN python -m pip install plotly==5.15.0 eventlet==0.36.1 SQLAlchemy==2.0.10 distlib==0.3.6 wheel==0.40.0 mysqlclient==2.1.1
RUN python -m pip install Flask-Migrate==4.0.4 mysqlclient==2.1.1 nbconvert==7.8.0 python-dotenv==1.0.0 Flask-SQLAlchemy==3.1.1

# Expose the default Flask port
EXPOSE 5000

# Run the Flask app
CMD ["python", "main.py"]
