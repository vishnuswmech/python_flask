
# Python Flask CRUD Application

This repository contains a Python Flask-based CRUD (Create, Read, Update, Delete) application. The project is containerized using Docker, integrates with Redis for caching, and can be deployed to Kubernetes using Helm.

## Features

- Flask-based REST API for CRUD operations
- Dockerized for containerization
- Redis integration for caching
- Kubernetes Helm charts for deployment
- HTML templates for user interaction

## Prerequisites

To run this project, you need the following tools installed:

- **Python 3.8+**
- **Docker**: For containerizing the application
- **Redis**: For caching
- **Kubernetes with Helm**: For deployment

## Project Structure

```bash
/
├── /create/app.py                           # Flask app for 'create' operation
├── /create/Dockerfile                       # Dockerfile for 'create' service
├── /home/app.py                             # Flask app for home page
├── /home/Dockerfile                         # Dockerfile for 'home' service
├── /read/app.py                             # Flask app for 'read' operation
├── /read/Dockerfile                         # Dockerfile for 'read' service
├── /update/app.py                           # Flask app for 'update' operation
├── /update/Dockerfile                       # Dockerfile for 'update' service
├── /delete/app.py                           # Flask app for 'delete' operation
├── /delete/Dockerfile                       # Dockerfile for 'delete' service
├── /redis/redis.conf                        # Redis configuration file
├── /redis/Dockerfile                        # Dockerfile for Redis service
├── /templates/form.html                     # HTML form for create/update operations
├── /templates/list.html                     # HTML template for listing items
├── /templates/error.html                    # HTML template for error page
├── /Helm/Chart.yaml                         # Helm chart metadata
├── /Helm/values.yaml                        # Default Helm values
├── /Helm/templates/deployment.yaml          # Kubernetes Deployment configuration
├── /Helm/templates/service.yaml             # Kubernetes Service definition
├── /Dockerfile                              # Dockerfile for the entire app
├── /requirements.txt                        # Python dependencies
└── /README.md                               # Project README (this file)
```

## Installation and Setup

### 1. Clone the Repository

To get started, clone the repository to your local machine:

```bash
git clone https://github.com/vishnuswmech/python_flask.git
cd python_flask
```

### 2. Set Up Python Environment

It’s recommended to use a virtual environment to isolate dependencies. Install Python dependencies from `requirements.txt`:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Running the Application Locally

Navigate to each service directory (e.g., `/create`, `/read`, etc.) and start the Flask app. Here’s an example for the **create** service:

```bash
cd /create
export FLASK_APP=app.py
flask run
```

Repeat for other services (`home`, `read`, `update`, `delete`) by navigating to each respective directory and running the app.

## Docker Setup

### 1. Build Docker Images

Each service has its own Dockerfile located in its directory. You can build Docker images for each service like this:

```bash
# For the create service
cd /create
docker build -t create-service .

# For the read service
cd /read
docker build -t read-service .

# Repeat for update, delete, home
```

### 2. Run Docker Containers

After building Docker images, you can run each service in a container:

```bash
# Run the create service container
docker run -d -p 5000:5000 create-service

# Run the read service container
docker run -d -p 5001:5000 read-service
```

Repeat this for other services (`home`, `update`, `delete`).

## Kubernetes Deployment

### 1. Helm Chart Deployment

The application is configured to be deployed using Helm. Make sure you have a Kubernetes cluster and Helm installed. To deploy the app:

```bash
# Deploy the application using Helm
cd /Helm
helm install crud-app .
```

### 2. Accessing the Application

After deployment, you can access each service through the NodePort or Ingress (depending on your configuration).

## Redis Integration

The application uses Redis as a caching mechanism. The Redis configuration is located in `/redis/redis.conf`, and a Dockerfile is provided to containerize Redis. Build and run Redis as follows:

```bash
cd /redis
docker build -t redis-service .
docker run -d -p 6379:6379 redis-service
```
