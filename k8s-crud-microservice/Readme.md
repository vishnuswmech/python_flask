# Deploying a CRUD Microservice using ArgoCD and GitHub Actions

## Project Overview:

This project focuses on deploying a CRUD microservice developed with Python Flask, utilizing HTML forms for the frontend. The microservice, initially containerized using Docker, will now be deployed in a Kubernetes (K8s) environment via a CI/CD pipeline. GitHub Actions will handle Continuous Integration (CI), while ArgoCD will manage Continuous Delivery (CD).

## Application Architecture:

The CRUD application comprises six microservices, each responsible for key operations: Create, Read, Update, and Delete.

- **Home**: Serves as the dashboard for accessing all other services.
- **Create**: Handles user data creation.
- **Read**: Retrieves existing data.
- **Update**: Modifies existing data.
- **Delete**: Removes data.
- **Redis**: Acts as the database server for data storage.

## Deployment Workflow:

1. Build Docker images for all services using GitHub Actions.
2. Update image tags in the `values.yaml` file of the Helm charts via GitHub Actions.
3. Deploy the Helm chart to the Kubernetes cluster using ArgoCD.

## Tech stack:
1. HTML forms
2. Python Flask
3. Helm charts
4. K8s
5. Rancher
6. Github actions
7. ArgoCD

## References:

- [GitHub Actions Workflow file](https://github.com/vishnuswmech/python_flask/blob/main/.github/workflows/docker-image-build.yml)
- [Helm Charts](https://github.com/vishnuswmech/python_flask/tree/main/k8s-crud-microservice/deploy/helm-charts)
- [ArgoCD Configuration](https://github.com/vishnuswmech/python_flask/blob/main/k8s-crud-microservice/deploy/argocd.yaml)
- [Code Repository](https://github.com/vishnuswmech/python_flask/tree/main/k8s-crud-microservice/build/code)
- [Initial containerization references](https://www.linkedin.com/posts/sri-vishnuvardhan_docker-python-flask-activity-7239552589313236992-KasI?utm_source=share&utm_medium=member_desktop)
