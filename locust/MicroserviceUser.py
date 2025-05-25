import random
import json
import os
from datetime import datetime
from locust import HttpUser, task, between
from locust.exception import RescheduleTask
import dotenv

class MicroserviceUser(HttpUser):
    """
    Clase base para pruebas de estrés de microservicios
    Simula usuarios reales interactuando con múltiples servicios
    """
    
    # Tiempo de espera entre requests (1-2 segundos como en tu configuración original)
    wait_time = between(1, 2)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setup_host()
        self.user_pool = []  # Pool de usuarios para reutilizar
        self.order_pool = []  # Pool de órdenes creadas
        self.product_pool = []  # Pool de productos disponibles
    
    def setup_host(self):
        """
        Configuración del host desde variables de entorno o archivo .env
        Prioridad: ENV_VAR > .env file > default
        """
        host = os.getenv('HOST')
        
        if not host:
            # Intenta cargar desde archivo .env para desarrollo local
            host_from_dotenv = dotenv.get_key('.env', 'HOST')
            if host_from_dotenv:
                host = host_from_dotenv
            else:
                # Fallback por defecto
                host = "http://localhost:8080"
                print(f"Warning: HOST not set. Using default: {host}")
        
        self.host = host
    
    def on_start(self):
        """
        Ejecutado al inicio de cada usuario simulado
        Inicializa datos de prueba y estado del usuario
        """
        # Generar datos de usuario único
        self.user_data = {
            "userId": random.randint(1000, 99999),
            "firstName": f"TestUser{random.randint(1, 1000)}",
            "lastName": f"LastName{random.randint(1, 1000)}",
            "email": f"test{random.randint(1, 10000)}@loadtest.com",
            "phone": f"+216{random.randint(10000000, 99999999)}"
        }
        
        # Headers comunes para todas las requests
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "Locust-LoadTest/1.0"
        }
        
        # Inicializar pools de datos
        self.initialize_data_pools()
    
    def initialize_data_pools(self):
        """Inicializa pools de datos para reutilización eficiente"""
        # Pool de productos (IDs que sabemos que existen)
        self.product_pool = list(range(1, 21))  # IDs 1-20
        
        # Pool de usuarios base
        self.user_pool = [
            {"userId": i, "firstName": f"User{i}", "lastName": f"Test{i}"} 
            for i in range(1, 11)
        ]
    
    def generate_timestamp(self):
        """Genera timestamp en el formato esperado por tus servicios"""
        now = datetime.now()
        return now.strftime("%d-%m-%Y__%H:%M:%S:%f")
    
    def get_random_product_data(self):
        """Genera datos de producto aleatorios pero consistentes"""
        product_id = random.choice(self.product_pool)
        return {
            "productId": product_id,
            "productTitle": random.choice(["Asus", "Samsung", "Apple", "Dell", "HP"]),
            "imageUrl": "https://example.com/product.jpg",
            "sku": f"SKU{random.randint(100000, 999999)}",
            "priceUnit": round(random.uniform(10.0, 2000.0), 2),
            "quantity": random.randint(1, 100)
        }

    # CASO DE USO 1: CONSULTAR PRODUCTOS
    @task(4)  # Peso 4 - Operación más frecuente (lectura)
    def get_products(self):
        """
        Consulta el catálogo de productos
        Simula navegación y búsqueda de productos
        """
        endpoints = [
            "/product-service/api/products",  # Lista todos los productos
            f"/product-service/api/products/{random.choice(self.product_pool)}",  # Producto específico
            "/product-service/api/products?category=electronics",  # Filtro por categoría
            f"/product-service/api/products?search=test{random.randint(1,5)}"  # Búsqueda
        ]
        
        endpoint = random.choice(endpoints)
        
        with self.client.get(endpoint, headers=self.headers, catch_response=True) as response:
            if response.status_code == 200:
                response.success()
                # Actualizar pool de productos si obtenemos datos reales
                try:
                    if "products" in response.text:
                        products = response.json()
                        if isinstance(products, list) and products:
                            self.product_pool.extend([p.get("productId") for p in products[:5]])
                except:
                    pass
            elif response.status_code == 404:
                response.success()  # 404 es esperado para algunos productos
            else:
                response.failure(f"Unexpected status code: {response.status_code}")

    # CASO DE USO 2: CREAR ÓRDENES
    @task(3)  # Peso 3 - Operación crítica del negocio
    def post_order(self):
        """
        Crea nuevas órdenes de compra
        Simula el proceso de checkout del usuario
        """
        order_id = random.randint(1000, 99999)
        
        order_data = {
            "orderId": order_id,
            "orderDate": self.generate_timestamp(),
            "orderDesc": random.choice([
                "Electronics purchase",
                "Bulk order",
                "Regular purchase",
                "Promotional order"
            ]),
            "orderFee": round(random.uniform(100, 5000), 2),
            "cart": {
                "cartId": random.randint(1, 1000),
                "userId": random.choice(self.user_pool)["userId"] if self.user_pool else 1
            }
        }
        
        with self.client.post(
            "/order-service/api/orders",
            json=order_data,
            headers=self.headers,
            catch_response=True
        ) as response:
            if response.status_code in [200, 201]:
                response.success()
                # Agregar orden al pool para uso posterior
                self.order_pool.append({
                    "orderId": order_id,
                    "orderDate": order_data["orderDate"],
                    "orderDesc": order_data["orderDesc"],
                    "orderFee": order_data["orderFee"]
                })
                # Mantener pool limitado para memoria
                if len(self.order_pool) > 10:
                    self.order_pool.pop(0)
            else:
                response.failure(f"Order creation failed: {response.status_code}")

    # CASO DE USO 3: SOLICITAR ENVÍOS
    @task(2)  # Peso 2 - Depende de órdenes exitosas
    def post_shipping(self):
        """
        Crea solicitudes de envío para órdenes
        Integra datos de productos y órdenes existentes
        """
        product_data = self.get_random_product_data()
        
        # Usar orden del pool si existe, sino crear datos básicos
        if self.order_pool:
            order_data = random.choice(self.order_pool)
        else:
            order_data = {
                "orderId": random.randint(1, 100),
                "orderDate": self.generate_timestamp(),
                "orderDesc": "Default order for shipping",
                "orderFee": 1000
            }
        
        shipping_data = {
            "productId": product_data["productId"],
            "orderId": order_data["orderId"],
            "orderedQuantity": random.randint(1, 5),
            "product": product_data,
            "order": order_data
        }
        
        with self.client.post(
            "/shipping-service/api/shippings",
            json=shipping_data,
            headers=self.headers,
            catch_response=True
        ) as response:
            if response.status_code in [200, 201]:
                response.success()
            elif response.status_code == 400:
                response.failure("Bad request - possibly invalid order/product relationship")
            else:
                response.failure(f"Shipping creation failed: {response.status_code}")

    # CASO DE USO 4: AÑADIR PRODUCTOS A FAVORITOS
    @task(2)  # Peso 2 - Funcionalidad de usuario frecuente
    def post_favorites(self):
        """
        Añade productos a la lista de favoritos del usuario
        Simula interacción social con productos
        """
        user_data = random.choice(self.user_pool) if self.user_pool else {
            "userId": 1,
            "firstName": "selim",
            "lastName": "horri"
        }
        
        product_data = self.get_random_product_data()
        
        favorites_data = {
            "userId": user_data["userId"],
            "productId": product_data["productId"],
            "likeDate": self.generate_timestamp(),
            "user": {
                "userId": user_data["userId"],
                "firstName": user_data["firstName"],
                "lastName": user_data["lastName"],
                "imageUrl": "https://bootdey.com/img/Content/avatar/avatar7.png",
                "email": f"user{user_data['userId']}@test.com",
                "phone": f"+216{random.randint(10000000, 99999999)}"
            },
            "product": product_data
        }
        
        with self.client.post(
            "/favourite-service/api/favourites",
            json=favorites_data,
            headers=self.headers,
            catch_response=True
        ) as response:
            if response.status_code in [200, 201]:
                response.success()
            elif response.status_code == 409:
                response.success()  # Conflicto esperado si ya existe
            else:
                response.failure(f"Favorite creation failed: {response.status_code}")

    # CASO DE USO 5: HACER PAGOS
    @task(3)  # Peso 3 - Proceso crítico de monetización
    def post_payment(self):
        """
        Procesa pagos para órdenes
        Simula diferentes estados de pago
        """
        payment_id = random.randint(1000, 99999)
        
        # Usar orden del pool si existe
        if self.order_pool:
            order_data = random.choice(self.order_pool)
        else:
            order_data = {
                "orderId": random.randint(1, 100),
                "orderDate": self.generate_timestamp(),
                "orderDesc": "Payment test order",
                "orderFee": round(random.uniform(100, 5000), 2)
            }
        
        payment_data = {
            "paymentId": payment_id,
            "isPayed": random.choice([True, False]),
            "paymentStatus": random.choice([
                "IN_PROGRESS", 
                "COMPLETED", 
                "FAILED", 
                "PENDING"
            ]),
            "order": order_data
        }
        
        with self.client.post(
            "/payment-service/api/payments",
            json=payment_data,
            headers=self.headers,
            catch_response=True
        ) as response:
            if response.status_code in [200, 201]:
                response.success()
            elif response.status_code == 402:  # Payment required
                response.success()  # Estado esperado en algunos casos
            else:
                response.failure(f"Payment processing failed: {response.status_code}")

    # CASO DE USO 6: REGISTRAR USUARIOS
    @task(1)  # Peso 1 - Operación menos frecuente pero importante
    def post_user(self):
        """
        Registra nuevos usuarios en el sistema
        Incluye creación de credenciales de autenticación
        """
        user_id = random.randint(1000, 99999)
        credential_id = random.randint(1000, 99999)
        
        user_data = {
            "userId": user_id,
            "firstName": f"LoadTest{random.randint(1, 1000)}",
            "lastName": f"User{random.randint(1, 1000)}",
            "imageUrl": f"https://bootdey.com/img/Content/avatar/avatar{random.randint(1,8)}.png",
            "email": f"loadtest{user_id}@testing.com",
            "phone": f"+216{random.randint(10000000, 99999999)}",
            "credential": {
                "credentialId": credential_id,
                "username": f"testuser{user_id}",
                "password": "testpass123",  # En producción, esto sería hasheado
                "roleBasedAuthority": random.choice(["ROLE_USER", "ROLE_PREMIUM_USER"]),
                "isEnabled": True,
                "isAccountNonExpired": True,
                "isAccountNonLocked": True,
                "isCredentialsNonExpired": True
            }
        }
        
        with self.client.post(
            "/user-service/api/users",
            json=user_data,
            headers=self.headers,
            catch_response=True
        ) as response:
            if response.status_code in [200, 201]:
                response.success()
                # Agregar usuario al pool para uso posterior
                self.user_pool.append({
                    "userId": user_id,
                    "firstName": user_data["firstName"],
                    "lastName": user_data["lastName"]
                })
                # Mantener pool limitado
                if len(self.user_pool) > 20:
                    self.user_pool.pop(0)
            elif response.status_code == 409:
                response.success()  # Usuario ya existe - esperado en pruebas
            else:
                response.failure(f"User creation failed: {response.status_code}")

    # HEALTH CHECKS Y MONITOREO
    @task(1)  # Peso 1 - Monitoreo constante
    def health_checks(self):
        """
        Verifica el estado de salud de todos los microservicios
        Detecta problemas de conectividad y disponibilidad
        """
        services = [
            "product-service",
            "order-service", 
            "shipping-service",
            "favourite-service",
            "payment-service",
            "user-service"
        ]
        
        service = random.choice(services)
        health_endpoints = [
            f"/{service}/actuator/health",
            f"/{service}/health",
            f"/{service}/api/health"
        ]
        
        for endpoint in health_endpoints:
            with self.client.get(endpoint, headers=self.headers, catch_response=True) as response:
                if response.status_code == 200:
                    response.success()
                    break
                elif response.status_code == 404:
                    continue  # Probar siguiente endpoint
                else:
                    response.failure(f"Health check failed for {service}: {response.status_code}")
                    break

    # FLUJO COMPLETO DE USUARIO
    @task(1)  # Peso 1 - Simula comportamiento real
    def complete_user_flow(self):
        """
        Simula un flujo completo de usuario desde navegación hasta pago
        Útil para detectar problemas de integración entre servicios
        """
        try:
            # 1. Buscar productos
            with self.client.get("/product-service/api/products", headers=self.headers) as response:
                if response.status_code != 200:
                    return
            
            # 2. Crear orden
            order_id = random.randint(10000, 99999)
            order_data = {
                "orderId": order_id,
                "orderDate": self.generate_timestamp(),
                "orderDesc": "Complete flow test order",
                "orderFee": 299.99,
                "cart": {"cartId": 1, "userId": self.user_data["userId"]}
            }
            
            with self.client.post("/order-service/api/orders", json=order_data, headers=self.headers) as response:
                if response.status_code not in [200, 201]:
                    return
            
            # 3. Procesar pago
            payment_data = {
                "paymentId": random.randint(10000, 99999),
                "isPayed": True,
                "paymentStatus": "COMPLETED",
                "order": order_data
            }
            
            with self.client.post("/payment-service/api/payments", json=payment_data, headers=self.headers) as response:
                if response.status_code not in [200, 201]:
                    return
                    
            # 4. Solicitar envío
            shipping_data = {
                "productId": random.choice(self.product_pool),
                "orderId": order_id,
                "orderedQuantity": 1,
                "product": self.get_random_product_data(),
                "order": order_data
            }
            
            self.client.post("/shipping-service/api/shippings", json=shipping_data, headers=self.headers)
            
        except Exception as e:
            print(f"Error in complete flow: {e}")

# DIFERENTES TIPOS DE USUARIOS PARA PATRONES DE CARGA VARIADOS

class LightUser(MicroserviceUser):
    """
    Usuario con carga ligera - Simula navegación casual
    Mayor tiempo de espera entre acciones
    """
    wait_time = between(3, 8)
    weight = 3  # 75% de los usuarios serán de este tipo
    
    # Solo tareas de lectura principalmente
    @task(10)
    def browse_products(self):
        self.get_products()
    
    @task(1)
    def occasional_favorite(self):
        self.post_favorites()

class HeavyUser(MicroserviceUser):
    """
    Usuario con carga pesada - Simula usuarios muy activos
    Menor tiempo de espera, más transacciones
    """
    wait_time = between(0.5, 1.5)
    weight = 1  # 25% de los usuarios serán de este tipo
    
    @task(5)
    def frequent_orders(self):
        self.post_order()
    
    @task(3)
    def frequent_payments(self):
        self.post_payment()
    
    @task(2)
    def check_everything(self):
        """Usuario power que revisa todo constantemente"""
        self.get_products()
        self.health_checks()

# USUARIO PARA PRUEBAS DE INTEGRACIÓN
class IntegrationTestUser(MicroserviceUser):
    """
    Usuario enfocado en probar integraciones entre servicios
    Ejecuta principalmente flujos completos
    """
    wait_time = between(2, 4)
    weight = 1
    
    @task(5)
    def integration_flows(self):
        self.complete_user_flow()
    
    @task(1)
    def service_health(self):
        self.health_checks()