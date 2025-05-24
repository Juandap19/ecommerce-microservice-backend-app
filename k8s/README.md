# Despliegue de eCommerce Microservices en Kubernetes

Este directorio contiene los archivos de configuración necesarios para desplegar la aplicación eCommerce Microservices en Kubernetes.

## Estructura de configuración

### Enfoque de configuración centralizada

Para simplificar la gestión de configuraciones, este proyecto utiliza un enfoque centralizado:

- **common-config.yaml**: Un único ConfigMap que contiene:
  - Configuraciones compartidas por todos los microservicios (conexiones a servicios, base de datos, logging)
  - Secciones específicas para cada microservicio
  - Variables de configuración en formato properties

En los Deployments, usamos:
- Variables de entorno para parámetros críticos y específicos
- Volúmenes montados para acceder al ConfigMap común

Este enfoque minimiza la duplicación de configuración y facilita la gestión centralizada de parámetros.

## Estructura de directorios

```
k8s/
  ├── common-config.yaml          # ConfigMap centralizado para todos los microservicios
  ├── namespace.yaml              # Definición del namespace
  ├── api-gateway/                # API Gateway
  │   ├── deployment.yaml         # Configuración del despliegue
  │   ├── service.yaml            # Definición del servicio
  │   ├── ingress.yaml            # Configuración de ingress para acceso externo
  │   └── kustomization.yaml      # Organización de recursos
  ├── order-service/              # Order Service
  │   ├── deployment.yaml         # Configuración del despliegue
  │   ├── service.yaml            # Definición del servicio
  │   └── kustomization.yaml      # Organización de recursos
  ├── favourite-service/          # Favourite Service
  │   ├── deployment.yaml         # Configuración del despliegue
  │   ├── service.yaml            # Definición del servicio
  │   └── kustomization.yaml      # Organización de recursos
  └── ... (otros servicios con estructura similar)
```

## Pasos para el despliegue

### 1. Crear el namespace y la configuración común

```bash
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/common-config.yaml
```

### 2. Desplegar los servicios de infraestructura

```bash
kubectl apply -k k8s/service-discovery/
kubectl apply -k k8s/cloud-config/
```

### 3. Desplegar el API Gateway y los microservicios

```bash
kubectl apply -k k8s/api-gateway/
kubectl apply -k k8s/order-service/
kubectl apply -k k8s/favourite-service/
# ... continuar con otros servicios
```

### 4. Verificar el despliegue

```bash
kubectl get pods -n ecommerce-app
kubectl get services -n ecommerce-app
```

## Acceso a la aplicación

Para acceder a la aplicación a través del API Gateway:

```bash
kubectl port-forward -n ecommerce-app svc/api-gateway 8080:8080
```

## Actualización de configuración

Para actualizar la configuración de todos los servicios, simplemente edita el ConfigMap común:

```bash
kubectl edit configmap -n ecommerce-app common-config
```

O aplica una nueva versión:

```bash
kubectl apply -f k8s/common-config.yaml
```

## Monitoreo

Para verificar los logs de un servicio específico:

```bash
kubectl logs -n ecommerce-app deployment/[nombre-servicio]
``` 