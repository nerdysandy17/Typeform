# Help Centre API - Helm Chart

This directory contains Helm chart configuration files for deploying the Help Centre API FastAPI application to Kubernetes.

## Overview

This Helm chart provides a production-ready configuration for deploying the FastAPI application with:
- Kubernetes Deployment for running the application
- Service for internal cluster communication
- Ingress for external HTTP/HTTPS access
- Horizontal Pod Autoscaler (HPA) for automatic scaling
- Secret management for API keys
- Health checks (liveness and readiness probes)
- Security contexts and best practices

## Chart Structure

```
helm/
├── Chart.yaml                    # Chart metadata
├── values.yaml                   # Default configuration values
├── README.md                     # This file
└── templates/
    ├── deployment.yaml           # Kubernetes Deployment
    ├── service.yaml              # Kubernetes Service
    ├── ingress.yaml              # Ingress for external access
    ├── serviceaccount.yaml       # Service Account
    ├── secret.yaml               # Secrets for API keys
    ├── hpa.yaml                  # Horizontal Pod Autoscaler
    └── _helpers.tpl              # Template helpers
```

## Key Features Demonstrated

### 1. **Deployment Configuration**
- **Replicas**: Configured for 2 replicas by default for high availability
- **Health Checks**: Liveness and readiness probes on the `/` endpoint
- **Resource Limits**: CPU and memory limits/requests defined
- **Security Context**: Non-root user, dropped capabilities

### 2. **Service & Ingress**
- **Service Type**: ClusterIP for internal cluster access
- **Ingress**: Configured with TLS/SSL support and cert-manager integration
- **External Access**: Ready for production domain configuration

### 3. **Secret Management**
- Kubernetes Secrets for sensitive data (API keys)
- Environment variables injected from secrets
- Production-ready pattern (can integrate with Vault, AWS Secrets Manager, etc.)

### 4. **Autoscaling**
- HPA configuration for automatic scaling based on CPU/memory
- Min/max replica configuration
- Disabled by default (can be enabled in values.yaml)

### 5. **Best Practices**
- Templated configurations using Helm helpers
- Separation of configuration (values.yaml) from templates
- Security contexts and least-privilege principles
- Resource management and limits

## Installation

### Prerequisites
- Kubernetes cluster (1.19+)
- Helm 3.x installed
- kubectl configured to access your cluster

### Install the Chart

```bash
# Create namespace
kubectl create namespace help-centre-api

# Add your API keys to the secret (encode in base64)
echo -n "your-openai-api-key" | base64
echo -n "your-pinecone-api-key" | base64

# Edit helm/templates/secret.yaml with the base64 values

# Install the chart
helm install help-centre-api ./helm \
  --namespace help-centre-api \
  --create-namespace

# Or install with custom values
helm install help-centre-api ./helm \
  --namespace help-centre-api \
  --set image.tag=v1.0.0 \
  --set ingress.hosts[0].host=api.yourdomain.com
```

### Upgrade Deployment

```bash
helm upgrade help-centre-api ./helm \
  --namespace help-centre-api \
  --set image.tag=v1.0.1
```

### Uninstall

```bash
helm uninstall help-centre-api --namespace help-centre-api
```

## Configuration

Key configuration options in `values.yaml`:

| Parameter | Description | Default |
|-----------|-------------|---------|
| `replicaCount` | Number of pod replicas | `2` |
| `image.repository` | Docker image repository | `help-centre-api` |
| `image.tag` | Docker image tag | `latest` |
| `service.type` | Kubernetes service type | `ClusterIP` |
| `service.port` | Service port | `80` |
| `ingress.enabled` | Enable ingress | `true` |
| `ingress.hosts[0].host` | Ingress hostname | `help-centre-api.example.com` |
| `resources.limits.cpu` | CPU limit | `500m` |
| `resources.limits.memory` | Memory limit | `512Mi` |
| `autoscaling.enabled` | Enable HPA | `false` |

## Local Development vs. Kubernetes

### Running Locally (Docker)

```bash
# Build image
docker build -t help-centre-api:latest .

# Run with Docker
docker run -p 80:80 --env-file .env help-centre-api:latest

# Access at http://localhost/docs
```

### Running on Kubernetes (Helm)

```bash
# Build and push image to registry
docker build -t your-registry/help-centre-api:v1.0.0 .
docker push your-registry/help-centre-api:v1.0.0

# Update values.yaml with your image repository
helm install help-centre-api ./helm \
  --set image.repository=your-registry/help-centre-api \
  --set image.tag=v1.0.0

# Access via ingress hostname configured in values.yaml
```

## Production Considerations

While this is a basic implementation, for production you should consider:

1. **Secret Management**: Use external secret managers (AWS Secrets Manager, HashiCorp Vault, Sealed Secrets)
2. **Image Registry**: Use a private container registry (ECR, GCR, ACR, Harbor)
3. **Monitoring**: Add Prometheus metrics and Grafana dashboards
4. **Logging**: Configure centralized logging (ELK stack, Loki)
5. **CI/CD**: Integrate with your CI/CD pipeline for automated deployments
6. **TLS Certificates**: Configure cert-manager for automatic SSL certificate management
7. **Network Policies**: Add network policies for pod-to-pod communication security
8. **Resource Quotas**: Set namespace resource quotas
9. **Backup**: Configure backup strategies for persistent data

## Validation

Test the Helm chart templates without installing:

```bash
# Render templates
helm template help-centre-api ./helm

# Validate with dry-run
helm install help-centre-api ./helm --dry-run --debug

# Lint the chart
helm lint ./helm
```

## Support

For issues or questions about the Helm configuration, please refer to:
- [Helm Documentation](https://helm.sh/docs/)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)


