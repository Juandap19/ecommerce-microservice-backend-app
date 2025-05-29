Aquí tienes una versión mejorada y traducida al inglés del README, con mejor estructura, redacción profesional, claridad técnica y estilo markdown moderno:

---

# 🛒 **eCommerce Microservices Project Documentation**

## 1. 📘 Introduction

### 1.1 🎯 Workshop Objectives

This workshop aims to guide the development of a **robust, scalable microservices architecture** for an eCommerce system, following industry best practices in software engineering. Beyond implementation, the goal is to foster a deep understanding of:

* Microservices principles
* DevOps culture and automation
* Software quality and observability

**Key goals include:**

* ✅ Designing a decoupled and scalable architecture
* 🔁 Automating the entire software lifecycle
* 📦 Ensuring portability and configuration consistency
* 🚀 Orchestrating and managing services in production
* 🧪 Adopting a comprehensive testing strategy
* 🔍 Guaranteeing observability and traceability

---

## 2. 🧩 Architecture Overview

### 2.1 🧱 Microservices Breakdown

This system consists of **10 core business microservices** and **3 infrastructure services**, each responsible for a specific domain in the eCommerce ecosystem.

#### 🔹 Business Microservices

| **Service**         | **Port** | **Responsibility & Justification**                                                                       |
| ------------------- | -------- | -------------------------------------------------------------------------------------------------------- |
| `user-service`      | 8700     | Handles user management (registration, auth, profiles). Decoupled for scalability and enhanced security. |
| `product-service`   | 8500     | Manages the product catalog and inventory. High throughput service.                                      |
| `order-service`     | 8300     | Responsible for order processing and management. Requires strong data consistency.                       |
| `payment-service`   | 8400     | Handles financial transactions. Isolated for security (PCI-DSS) and third-party payment integration.     |
| `shipping-service`  | 8600     | Manages shipping and logistics. Easily integrates with external transport services.                      |
| `favourite-service` | 8800     | Manages user favorite lists. Lightweight, independently scalable.                                        |

#### 🛠 Infrastructure Services

| **Service**                  | **Port** | **Purpose**                                                                         |
| ---------------------------- | -------- | ----------------------------------------------------------------------------------- |
| `service-discovery` (Eureka) | 8761     | Enables dynamic service registration and discovery.                                 |
| `cloud-config`               | 9296     | Centralized external configuration. Ensures consistency across environments.        |
| `api-gateway`                | -        | Single entry point with routing, authentication, rate limiting, and load balancing. |

#### ⚙️ Supporting Services

| **Service**    | **Port** | **Purpose**                                                                  |
| -------------- | -------- | ---------------------------------------------------------------------------- |
| `proxy-client` | -        | Simplifies HTTP communication between services with circuit breakers.        |
| `zipkin`       | 9411     | Distributed tracing for monitoring and debugging multi-service interactions. |

---

## 3. 🧰 Tools & Technologies

### 🚀 Development & Frameworks

* **Spring Boot**: Core framework for microservices
* **Maven**: Dependency and build management
* **Java 11**: Stable LTS version

### 🛠 DevOps & CI/CD

* **Jenkins**: Automated CI/CD pipelines:

  * Maven build and packaging
  * Unit, integration, and E2E tests
  * Docker image build and push
  * Kubernetes deployment
* **Git**: Version control with branching strategy (`dev`, `stage`, `master`)

### 📦 Containerization & Orchestration

* **Docker**: Portable service containerization
* **Docker Hub**: Image registry
* **Kubernetes**: Service orchestration:

  * Deployments, Services, ConfigMaps
  * Health checks, rolling updates
  * Namespace isolation (`ecommerce`)

### ✅ Testing & Quality Assurance

* **JUnit**, **Spring Boot Test**: Unit and integration testing
* **Locust**: Load and stress testing (10–50 concurrent users)
* **Testcontainers**: Real-container integration testing

---

## 4. 🧭 System Architecture

### 4.1 🖼 Microservices Architecture Diagram

> *(Insert architecture image here)*
> A visual overview of service interactions, infrastructure components, and system scalability.

### 4.2 🔄 Service Interactions

* **API Gateway**: Handles routing, auth, load balancing
* **Eureka**: Enables dynamic service discovery
* **Cloud Config**: Centralized configuration without redeployment
* **Proxy Client**: Adds resilience with circuit breakers
* **Zipkin**: Traces cross-service HTTP requests
* **Internal HTTP Communication**: Managed via gateway and Eureka for loosely coupled services

### 4.3 🌍 Environments

| **Environment** | **Purpose**                     |
| --------------- | ------------------------------- |
| `dev`           | Development and experimentation |
| `stage`         | End-to-end integration testing  |
| `master`        | Stable production environment   |

Each environment has its own CI/CD pipeline and configuration.

---

## 5. ⚙️ Environment Setup

### 5.1 🧪 Jenkins (Local Windows Setup with UI)

* **Installation**: [Jenkins Download](https://www.jenkins.io/download/)
* **Initial Access**: Unlock with the auto-generated key
* **Recommended Plugins**: Docker Pipeline, Git, Blue Ocean
* **Pipeline Management**: Create & monitor jobs via UI
* **Declarative Pipeline**: All stages defined in `Jenkinsfile`
* **Automated Deployment**: CI/CD flow from build to Kubernetes deployment

> ✅ *Best Practices:*
>
> * Store secrets securely in Jenkins credentials
> * Grant Docker access permissions properly

### 5.2 🐳 Docker & Microservice Images

* One `Dockerfile` per microservice
* Lightweight base images for fast builds
* Local orchestration with `docker-compose`
* CI pipeline builds & pushes images to Docker Hub

### 5.3 ☸ Kubernetes

* YAML manifests define deployments, services, etc.
* Dedicated namespace: `ecommerce`
* Common commands:

  * `kubectl apply -f k8s/`
  * `kubectl get pods -n ecommerce`
  * `kubectl logs <pod-name> -n ecommerce`
* Jenkins automates post-build deployments

### 5.4 📁 Repository Structure

```
ecommerce-microservice-backend-app/
├── api-gateway/
├── cloud-config/
├── favourite-service/
├── order-service/
├── payment-service/
├── product-service/
├── proxy-client/
├── service-discovery/
├── shipping-service/
├── user-service/
├── zipkin/
├── k8s/
├── locust/
├── Jenkinsfile
├── compose.yml
└── README.md
```

---

## 6. 🔄 CI/CD Pipelines

> 🛠️ *COMING SOON:* Full breakdown of Jenkins pipelines with visual stages, rollback strategies, and blue-green deployment logic. (Pending section completion.)

---

## 7. 🧪 Testing Strategy

A **multi-layered testing strategy** ensures reliability, scalability, and business correctness across all services.

### 7.1 ✅ Unit Testing

Each service uses **JUnit** and **Mockito** to validate business logic in isolation.

| Service         | Test Class             | Example Methods Tested                |
| --------------- | ---------------------- | ------------------------------------- |
| user-service    | UserServiceImplTest    | `testFindById`, `testSave`            |
| product-service | ProductServiceImplTest | `testFindById_ShouldReturnProductDto` |
| payment-service | PaymentServiceImplTest | `testDeleteById`                      |

📌 *Example (user-service):*

```java
@Test
void testFindById() {
    Integer userId = 1;
    when(userRepository.findById(userId)).thenReturn(Optional.of(user));
    UserDto result = userServiceImpl.findById(userId);
    assertNotNull(result);
    assertEquals(userDto.getFirstName(), result.getFirstName());
}
```

### 7.2 🔌 Integration Testing

Validates interaction between layers using in-memory databases or containers.

📌 *Example (product-service):*

```java
@Test
public void testFindAllProducts() {
    ResponseEntity<DtoCollectionResponse> response = restTemplate.exchange(
        baseUrl, HttpMethod.GET, null, DtoCollectionResponse.class);
    assertEquals(HttpStatus.OK, response.getStatusCode());
}
```

### 7.3 🔁 End-to-End (E2E) Testing

Simulates complete business flows across multiple services.

📌 *Example (order-service):*

```java
@Test
void shouldGetOrderById() {
    int orderId = 2;
    ResponseEntity<String> response = restFacade.get(
        productServiceUrl + "/order-service/api/orders/" + orderId, String.class);
    assertTrue(response.getStatusCode().is2xxSuccessful());
}
```

### 7.4 📊 Load & Stress Testing (Locust)

Simulates user traffic to test system capacity and stability:

* **10 users** for load test
* **50 users** for stress test
* **CSV reports** with latency, throughput, and error rate metrics

---

## 📌 Conclusion

This microservices architecture enables:

* Independent deployment and scaling
* Fault isolation and resilience
* Complete DevOps automation
* Real-world testing coverage (unit, integration, E2E, performance)

With these principles in place, this eCommerce system is built for **growth, agility, and production-grade reliability**.

---

If you’d like, I can generate a PDF version or assist in creating diagrams or deployment charts. Let me know!
