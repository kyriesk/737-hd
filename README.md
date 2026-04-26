# Cloud-Native Flask API on GCP

## Project Goal

Build a simple cloud-native REST API using Python Flask, containerize it with Docker, store the image in Google Artifact Registry, deploy it to Google Kubernetes Engine (GKE), and automate the build and deployment workflow with Google Cloud Build.

## Application Overview

- `app.py`: Flask app exposing:
  - `GET /api/health`
  - `GET /api/message`
- `Dockerfile`: container image build definition
- `k8s/deployment.yaml`: Kubernetes Deployment for the API
- `k8s/service.yaml`: Kubernetes Service exposing the app internally
- `cloudbuild.yaml`: CI/CD pipeline definition for Cloud Build

## Architecture

1. Developer pushes code to Git source control.
2. Cloud Build triggers on commits and:
   - builds the Docker image
   - pushes it to Artifact Registry
   - updates the Kubernetes deployment on GKE
3. GKE runs the Flask container behind a ClusterIP service.

## Files

- `app.py` - Flask REST API implementation
- `requirements.txt` - Python dependencies
- `Dockerfile` - container build
- `cloudbuild.yaml` - CI/CD pipeline for build/deploy
- `k8s/deployment.yaml` - Deployment manifest
- `k8s/service.yaml` - ClusterIP Service manifest
- `.dockerignore` - files excluded from Docker build

## Deployment Instructions

1. Authenticate with Deakin GCP project:

   ```bash
   gcloud auth login
   gcloud config set project YOUR_PROJECT_ID
   ```

2. Enable required APIs:

   ```bash
   gcloud services enable artifactregistry.googleapis.com container.googleapis.com cloudbuild.googleapis.com
   ```

3. Create Artifact Registry repository:

   ```bash
   gcloud artifacts repositories create hd-repo \
     --repository-format=docker \
     --location=australia-southeast1
   ```

4. Create a GKE cluster (example):

   ```bash
   gcloud container clusters create hd-gke-cluster \
     --zone=australia-southeast1-a \
     --num-nodes=2
   ```

5. Deploy the Kubernetes manifests:

   ```bash
   kubectl apply -f k8s/deployment.yaml
   kubectl apply -f k8s/service.yaml
   ```

6. Use port-forwarding for safe access:
   ```bash
   kubectl port-forward service/hd-api-service 8080:80
   curl http://127.0.0.1:8080/api/health
   ```

## Cloud Build CI/CD

The `cloudbuild.yaml` pipeline performs:

- Docker build
- Docker push to Artifact Registry
- GKE cluster credentials retrieval
- `kubectl set image` to update the Deployment

Substitutions configured in `cloudbuild.yaml`:

- `_ARTIFACT_REGISTRY_HOST`: `australia-southeast1-docker.pkg.dev`
- `_REPOSITORY`: `hd-repo`
- `_CLUSTER_NAME`: `hd-gke-cluster`
- `_CLUSTER_ZONE`: `australia-southeast1-a`

## Security and Access

- Service type is `ClusterIP` to minimize unnecessary public exposure.
- Access can be controlled via `kubectl port-forward` or private/internal ingress.
- No credentials or service account keys are stored in source control.

## Implementation Plan

1. Build the Flask app and verify locally.
2. Containerize with Docker and validate the image.
3. Configure Artifact Registry and push the image.
4. Create the GKE cluster and apply Kubernetes manifests.
5. Create Cloud Build trigger and validate automated deployments.
6. Document the architecture, risks, and deployment commands.

## Risks

- GCP permission restrictions or missing APIs in the Deakin environment.
- Artifact Registry access denial or repository configuration issues.
- GKE cluster setup problems due to quota, region, or service account permissions.
- Cloud Build service account lacking `container.clusters.get` or `artifactregistry.repositories.downloadArtifacts`.

## Time Management Plan

- Day 1: create Flask app, Dockerfile, and Kubernetes manifests (1-2 hours).
- Day 2: configure GCP resources and validate deployment (1-2 hours).
- Day 3: configure Cloud Build, test pipeline, and finalize documentation (1 hour).
