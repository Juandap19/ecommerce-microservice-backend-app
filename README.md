
# 🛒 **eCommerce Microservices Project Documentation**

## 1. 📘 Introduction

### 1.1 🎯 Workshop Objectives

This workshop is designed to provide hands-on guidance in building a **resilient, scalable microservices architecture** tailored for modern eCommerce platforms, grounded in industry-proven software engineering practices. It goes beyond technical implementation to cultivate a deep, practical understanding of:

* Core microservices principles  
* DevOps culture and automation  
* Software quality, observability, and resilience  

**Primary objectives of the workshop include:**

* ✅ Designing a modular, decoupled architecture built for scalability  
* 🔁 Automating the end-to-end software delivery lifecycle  
* 📦 Ensuring environment consistency and deployment portability  
* 🚀 Managing and orchestrating services in production environments  
* 🧪 Implementing a robust, multi-level testing strategy  
* 🔍 Enabling full observability, traceability, and system introspection  



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

### 2.2 🎯 Justification for Service Selection and Integration Strategy
The selection of these services is strategic and intentional, as they reflect core business capabilities and critical integration flows within a modern eCommerce ecosystem. Their interdependencies make them ideal for implementing meaningful end-to-end (E2E) testing, robust observability, and scalable automation pipelines.

These services were chosen for the following key reasons:

* **Critical Business Coverage:**
Each business microservice encapsulates a distinct domain (e.g., user management, order processing, payments), collectively representing the primary customer journey. This granularity allows for focused development, testing, and scaling of each functional unit independently.

* **Integration-Oriented Architecture:**
Services like proxy-client and api-gateway act as integration facilitators. proxy-client orchestrates internal service-to-service communication (e.g., between user-service, product-service, and order-service), while implementing fault-tolerance patterns like circuit breakers. Meanwhile, api-gateway provides a secure and unified external interface, supporting routing, rate limiting, and load balancing.

* **Infrastructure Backbone:**
service-discovery (via Eureka) and cloud-config form the foundational infrastructure layer. They enable dynamic service registration, centralized configuration management, and environmental consistency, which are essential for operating at scale in a cloud-native setup.

* **Observability and Traceability:**
zipkin enables distributed tracing, a crucial aspect of maintaining visibility across asynchronous, multi-service interactions—especially under production load or in incident response scenarios.

* **Scalability and Independence:**
Lightweight services such as favourite-service can scale independently based on usage patterns. This is aligned with the microservices principle of autonomous deployability, reducing the blast radius of deployments and promoting agility.

## 3. 🧰 Tools & Technologies


#### 🚀 Development & Frameworks

- ![Spring Boot](https://img.shields.io/badge/-Spring%20Boot-6DB33F?style=flat&logo=spring-boot&logoColor=white) – **Core framework for microservices**

- ![Maven](https://img.shields.io/badge/-Maven-C71A36?style=flat&logo=apache-maven&logoColor=white)  – **Dependency and build management**

- ![Java](https://img.shields.io/badge/-Java%2011-007396?style=flat&logo=java&logoColor=white)  – **Stable LTS version** 

---

#### 🛠 DevOps & CI/CD

- ![Jenkins](https://img.shields.io/badge/-Jenkins-D24939?style=flat&logo=jenkins&logoColor=white)    -  **Automated CI/CD pipelines**:
  - Maven build and packaging  
  - Unit, integration, and E2E tests  
  - Docker image build and push  
  - Kubernetes deployment  

- ![Git](https://img.shields.io/badge/-Git-F05032?style=flat&logo=git&logoColor=white) - **Version control with branching strategy (`dev`, `stage`, `master`)**

---

#### 📦 Containerization & Orchestration

- ![Docker](https://img.shields.io/badge/-Docker-2496ED?style=flat&logo=docker&logoColor=white) – **Portable service containerization**  
- ![Docker Hub](https://img.shields.io/badge/-Docker%20Hub-0db7ed?style=flat&logo=docker&logoColor=white)  – **Image registry for CI/CD pipelines**  
- ![Kubernetes](https://img.shields.io/badge/-Kubernetes-326CE5?style=flat&logo=kubernetes&logoColor=white)  – **Service orchestration:**
  - Deployments, Services, ConfigMaps  
  - Health checks, rolling updates  
  - Namespace isolation (`ecommerce`)  

---

#### ✅ Testing & Quality Assurance

- ![JUnit](https://img.shields.io/badge/-JUnit&Locust-25A162?style=flat&logo=java&logoColor=white)  -  **Unit and integration testing** 
- ![Locust](https://img.shields.io/badge/-Locust-000000?style=flat&logo=python&logoColor=white)  - **Load and stress testing (10–50 concurrent users)**
- ![Testcontainers](https://img.shields.io/badge/-Testcontainers-0db7ed?style=flat&logo=docker&logoColor=white) -  **Real-container integration testing**

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


---

## 6. 🔄 CI/CD Pipelines 

> 🛠️ *COMING SOON:* Full breakdown of Jenkins pipelines with visual stages, rollback strategies, and blue-green deployment logic. (Pending section completion.)

---

## 7. 🧪 Testing Strategy


> 🛠️ *COMING SOON:* 
---

## 📌 Conclusion

> 🛠️ *COMING SOON:* 
