# Documentación del Proyecto djangov2 - API REST CRUD

## 📋 Resumen Ejecutivo

Se implementó una aplicación Django (`djangov2`) con una API REST completa que gestiona un sistema de e-commerce con 5 modelos principales. La API soporta operaciones CRUD (GET, POST, PUT, PATCH, DELETE) para todas las entidades y cuenta con validaciones integradas.

---

## 🗄️ Modelos Implementados

### 1. **Category** - Categorías de Productos
| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | Auto | ID único (auto-generado) |
| `name` | CharField | Nombre de la categoría (máx 100 caracteres) |
| `description` | TextField | Descripción detallada (opcional) |

### 2. **Product** - Productos del Catálogo
| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | Auto | ID único (auto-generado) |
| `category` | ForeignKey | Referencia a Category (ON DELETE: SET_NULL) |
| `name` | CharField | Nombre del producto (máx 200 caracteres) |
| `description` | TextField | Descripción del producto (opcional) |
| `price` | DecimalField | Precio en USD (máx 10 dígitos, 2 decimales) |
| `stock` | IntegerField | Cantidad disponible (mínimo 0) |
| `created_at` | DateTime | Fecha de creación (auto-generada) |

### 3. **Customer** - Clientes del Sistema
| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | Auto | ID único (auto-generado) |
| `first_name` | CharField | Nombre (máx 100 caracteres) |
| `last_name` | CharField | Apellido (máx 100 caracteres) |
| `email` | EmailField | Email único y validado |
| `phone` | CharField | Teléfono (máx 20 caracteres, opcional) |
| `created_at` | DateTime | Fecha de registro (auto-generada) |

### 4. **Order** - Órdenes de Compra
| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | Auto | ID único (auto-generado) |
| `customer` | ForeignKey | Referencia a Customer (ON DELETE: CASCADE) |
| `items` | JSONField | Lista de items [{product_id, quantity, price}] |
| `total` | DecimalField | Total de la orden (máx 12 dígitos, 2 decimales) |
| `status` | CharField | Estado: pending, paid, shipped, cancelled |
| `created_at` | DateTime | Fecha de creación (auto-generada) |

### 5. **Review** - Reseñas de Productos
| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | Auto | ID único (auto-generado) |
| `product` | ForeignKey | Referencia a Product (ON DELETE: CASCADE) |
| `customer` | ForeignKey | Referencia a Customer (opcional, ON DELETE: SET_NULL) |
| `rating` | PositiveSmallInteger | Calificación (1-5 estrellas) |
| `comment` | TextField | Comentario de la reseña (máx 1000 caracteres, opcional) |
| `created_at` | DateTime | Fecha de creación (auto-generada) |

---

## 🔌 Endpoints API

### **1. CATEGORIES - Gestión de Categorías**

#### 📌 GET `/api/categories/` - Listar todas las categorías
**Método:** GET  
**Respuesta (200 OK):**
```json
[
  {
    "id": 1,
    "name": "Electronics",
    "description": "Electronic devices and accessories"
  },
  {
    "id": 2,
    "name": "Books",
    "description": "Physical and digital books"
  }
]
```

#### 📌 POST `/api/categories/` - Crear nueva categoría
**Método:** POST  
**Body:**
```json
{
  "name": "Clothing",
  "description": "Men's and women's clothing"
}
```
**Respuesta (201 Created):**
```json
{
  "id": 3,
  "name": "Clothing",
  "description": "Men's and women's clothing"
}
```
**Errores:**
- `400 Bad Request`: Si el nombre está vacío o excede 100 caracteres

#### 📌 GET `/api/categories/{id}/` - Obtener categoría por ID
**Método:** GET  
**Respuesta (200 OK):**
```json
{
  "id": 1,
  "name": "Electronics",
  "description": "Electronic devices and accessories"
}
```
**Errores:**
- `404 Not Found`: Si la categoría no existe

#### 📌 PUT `/api/categories/{id}/` - Actualizar categoría completa
**Método:** PUT  
**Body:**
```json
{
  "name": "Tech & Electronics",
  "description": "All tech products"
}
```
**Respuesta (200 OK):**
```json
{
  "id": 1,
  "name": "Tech & Electronics",
  "description": "All tech products"
}
```

#### 📌 PATCH `/api/categories/{id}/` - Actualizar parcialmente
**Método:** PATCH  
**Body:**
```json
{
  "description": "Updated description only"
}
```
**Respuesta (200 OK):**
```json
{
  "id": 1,
  "name": "Electronics",
  "description": "Updated description only"
}
```

#### 📌 DELETE `/api/categories/{id}/` - Eliminar categoría
**Método:** DELETE  
**Respuesta:** 204 No Content  
**Errores:**
- `404 Not Found`: Si la categoría no existe

---

### **2. PRODUCTS - Gestión de Productos**

#### 📌 GET `/api/products/` - Listar todos los productos
**Método:** GET  
**Respuesta (200 OK):**
```json
[
  {
    "id": 1,
    "category": 1,
    "name": "Laptop Dell XPS",
    "description": "High-performance laptop",
    "price": "999.99",
    "stock": 5,
    "created_at": "2026-07-05T10:30:00Z"
  }
]
```

#### 📌 POST `/api/products/` - Crear nuevo producto
**Método:** POST  
**Body:**
```json
{
  "category": 1,
  "name": "Laptop HP Pavilion",
  "description": "Mid-range laptop",
  "price": "599.99",
  "stock": 15
}
```
**Respuesta (201 Created):**
```json
{
  "id": 2,
  "category": 1,
  "name": "Laptop HP Pavilion",
  "description": "Mid-range laptop",
  "price": "599.99",
  "stock": 15,
  "created_at": "2026-07-05T11:00:00Z"
}
```
**Errores:**
- `400 Bad Request`: 
  - Precio negativo
  - Stock negativo
  - Nombre vacío o > 200 caracteres
  - Category no existe

#### 📌 GET `/api/products/{id}/` - Obtener producto por ID
**Método:** GET  
**Respuesta (200 OK):**
```json
{
  "id": 1,
  "category": 1,
  "name": "Laptop Dell XPS",
  "description": "High-performance laptop",
  "price": "999.99",
  "stock": 5,
  "created_at": "2026-07-05T10:30:00Z"
}
```

#### 📌 PUT `/api/products/{id}/` - Actualizar producto
**Método:** PUT  
**Body:**
```json
{
  "category": 1,
  "name": "Laptop Dell XPS 15",
  "description": "Ultra high-performance laptop",
  "price": "1199.99",
  "stock": 3
}
```
**Respuesta (200 OK):**
```json
{
  "id": 1,
  "category": 1,
  "name": "Laptop Dell XPS 15",
  "description": "Ultra high-performance laptop",
  "price": "1199.99",
  "stock": 3,
  "created_at": "2026-07-05T10:30:00Z"
}
```

#### 📌 PATCH `/api/products/{id}/` - Actualización parcial
**Método:** PATCH  
**Body:**
```json
{
  "price": "1149.99",
  "stock": 2
}
```
**Respuesta (200 OK):** Producto actualizado

#### 📌 DELETE `/api/products/{id}/` - Eliminar producto
**Método:** DELETE  
**Respuesta:** 204 No Content

---

### **3. CUSTOMERS - Gestión de Clientes**

#### 📌 GET `/api/customers/` - Listar todos los clientes
**Método:** GET  
**Respuesta (200 OK):**
```json
[
  {
    "id": 1,
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@example.com",
    "phone": "1234567890",
    "created_at": "2026-07-05T09:00:00Z"
  }
]
```

#### 📌 POST `/api/customers/` - Crear nuevo cliente
**Método:** POST  
**Body:**
```json
{
  "first_name": "Jane",
  "last_name": "Smith",
  "email": "jane@example.com",
  "phone": "9876543210"
}
```
**Respuesta (201 Created):**
```json
{
  "id": 2,
  "first_name": "Jane",
  "last_name": "Smith",
  "email": "jane@example.com",
  "phone": "9876543210",
  "created_at": "2026-07-05T11:30:00Z"
}
```
**Errores:**
- `400 Bad Request`:
  - Email inválido o duplicado
  - Nombre o apellido vacío
  - Teléfono > 20 caracteres

#### 📌 GET `/api/customers/{id}/` - Obtener cliente por ID
**Método:** GET  
**Respuesta (200 OK):** Datos completos del cliente

#### 📌 PUT `/api/customers/{id}/` - Actualizar cliente
**Método:** PUT  
**Body:**
```json
{
  "first_name": "Jane",
  "last_name": "Johnson",
  "email": "jane.johnson@example.com",
  "phone": "5555555555"
}
```
**Respuesta (200 OK):** Cliente actualizado

#### 📌 PATCH `/api/customers/{id}/` - Actualización parcial
**Método:** PATCH  
**Body:**
```json
{
  "phone": "1111111111"
}
```
**Respuesta (200 OK):** Cliente actualizado

#### 📌 DELETE `/api/customers/{id}/` - Eliminar cliente
**Método:** DELETE  
**Respuesta:** 204 No Content

---

### **4. ORDERS - Gestión de Órdenes**

#### 📌 GET `/api/orders/` - Listar todas las órdenes
**Método:** GET  
**Respuesta (200 OK):**
```json
[
  {
    "id": 1,
    "customer": 1,
    "items": [
      {"product_id": 1, "quantity": 2, "price": "999.99"}
    ],
    "total": "1999.98",
    "status": "pending",
    "created_at": "2026-07-05T12:00:00Z"
  }
]
```

#### 📌 POST `/api/orders/` - Crear nueva orden
**Método:** POST  
**Body:**
```json
{
  "customer": 1,
  "items": [
    {"product_id": 1, "quantity": 1, "price": "999.99"},
    {"product_id": 2, "quantity": 2, "price": "599.99"}
  ],
  "total": "2199.97",
  "status": "pending"
}
```
**Respuesta (201 Created):**
```json
{
  "id": 2,
  "customer": 1,
  "items": [
    {"product_id": 1, "quantity": 1, "price": "999.99"},
    {"product_id": 2, "quantity": 2, "price": "599.99"}
  ],
  "total": "2199.97",
  "status": "pending",
  "created_at": "2026-07-05T13:00:00Z"
}
```
**Errores:**
- `400 Bad Request`:
  - Total negativo
  - Status inválido (solo: pending, paid, shipped, cancelled)
  - Items vacío o no es lista
  - Customer no existe

#### 📌 GET `/api/orders/{id}/` - Obtener orden por ID
**Método:** GET  
**Respuesta (200 OK):** Datos completos de la orden

#### 📌 PUT `/api/orders/{id}/` - Actualizar orden
**Método:** PUT  
**Body:**
```json
{
  "customer": 1,
  "items": [{"product_id": 1, "quantity": 1, "price": "999.99"}],
  "total": "999.99",
  "status": "paid"
}
```
**Respuesta (200 OK):** Orden actualizada

#### 📌 PATCH `/api/orders/{id}/` - Cambiar solo el estado
**Método:** PATCH  
**Body:**
```json
{
  "status": "shipped"
}
```
**Respuesta (200 OK):** Orden actualizada

#### 📌 DELETE `/api/orders/{id}/` - Eliminar orden
**Método:** DELETE  
**Respuesta:** 204 No Content

---

### **5. REVIEWS - Gestión de Reseñas**

#### 📌 GET `/api/reviews/` - Listar todas las reseñas
**Método:** GET  
**Respuesta (200 OK):**
```json
[
  {
    "id": 1,
    "product": 1,
    "customer": 1,
    "rating": 5,
    "comment": "Excellent product, highly recommended!",
    "created_at": "2026-07-05T14:00:00Z"
  }
]
```

#### 📌 POST `/api/reviews/` - Crear nueva reseña
**Método:** POST  
**Body:**
```json
{
  "product": 1,
  "customer": 1,
  "rating": 4,
  "comment": "Very good quality, but shipping took too long."
}
```
**Respuesta (201 Created):**
```json
{
  "id": 2,
  "product": 1,
  "customer": 1,
  "rating": 4,
  "comment": "Very good quality, but shipping took too long.",
  "created_at": "2026-07-05T14:30:00Z"
}
```
**Errores:**
- `400 Bad Request`:
  - Rating fuera de rango 1-5
  - Comentario > 1000 caracteres
  - Product no existe

#### 📌 GET `/api/reviews/{id}/` - Obtener reseña por ID
**Método:** GET  
**Respuesta (200 OK):** Datos completos de la reseña

#### 📌 PUT `/api/reviews/{id}/` - Actualizar reseña
**Método:** PUT  
**Body:**
```json
{
  "product": 1,
  "customer": 1,
  "rating": 5,
  "comment": "Updated: Excellent! Product arrived in perfect condition."
}
```
**Respuesta (200 OK):** Reseña actualizada

#### 📌 PATCH `/api/reviews/{id}/` - Cambiar solo la calificación
**Método:** PATCH  
**Body:**
```json
{
  "rating": 3
}
```
**Respuesta (200 OK):** Reseña actualizada

#### 📌 DELETE `/api/reviews/{id}/` - Eliminar reseña
**Método:** DELETE  
**Respuesta:** 204 No Content

---

## ✅ Validaciones Implementadas

### Category
- ✓ Nombre no puede estar vacío
- ✓ Nombre máximo 100 caracteres

### Product
- ✓ Precio no puede ser negativo
- ✓ Stock no puede ser negativo
- ✓ Nombre no puede estar vacío
- ✓ Nombre máximo 200 caracteres

### Customer
- ✓ Email válido y único
- ✓ Nombre no puede estar vacío
- ✓ Apellido no puede estar vacío
- ✓ Teléfono máximo 20 caracteres

### Order
- ✓ Total no puede ser negativo
- ✓ Status debe ser: pending, paid, shipped o cancelled
- ✓ Items debe ser una lista no vacía

### Review
- ✓ Rating debe estar entre 1 y 5
- ✓ Comentario máximo 1000 caracteres

---

## 🧪 Suite de Tests

Se implementó una suite completa de 60+ tests que cubren:
- ✅ Creación (POST) de todos los modelos
- ✅ Lectura (GET lista e individual) de todos los modelos
- ✅ Actualización (PUT y PATCH) de todos los modelos
- ✅ Eliminación (DELETE) de todos los modelos
- ✅ Validaciones y manejo de errores
- ✅ Casos de error (datos inválidos, duplicados, etc.)

### Ejecutar tests:
```powershell
cd c:\Users\jandry\OneDrive\Desktop\djangoapi
.venv\Scripts\python.exe manage.py test djangov2 -v 2
```

---

## 📝 Pasos de Configuración y Ejecución

### 1. **Preparar el Ambiente**
```powershell
cd c:\Users\jandry\OneDrive\Desktop\djangoapi
.venv\Scripts\python.exe -m pip install --upgrade pip
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### 2. **Crear Migraciones**
```powershell
.venv\Scripts\python.exe manage.py makemigrations
```

### 3. **Aplicar Migraciones**
```powershell
.venv\Scripts\python.exe manage.py migrate
```

### 4. **Crear Superusuario (Opcional, para admin)**
```powershell
.venv\Scripts\python.exe manage.py createsuperuser
```

### 5. **Ejecutar Servidor**
```powershell
.venv\Scripts\python.exe manage.py runserver
```
El servidor estará disponible en: **http://127.0.0.1:8000/**

### 6. **Acceder a la API**
- Todos los endpoints: **http://127.0.0.1:8000/api/**
- Admin Django: **http://127.0.0.1:8000/admin/**
- DRF Browsable API: **http://127.0.0.1:8000/api/** (en navegador)

---

## 🔍 Ejemplos con cURL

### Crear una categoría:
```bash
curl -X POST http://127.0.0.1:8000/api/categories/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Electronics", "description": "Tech products"}'
```

### Listar todos los productos:
```bash
curl -X GET http://127.0.0.1:8000/api/products/
```

### Obtener cliente por ID:
```bash
curl -X GET http://127.0.0.1:8000/api/customers/1/
```

### Actualizar una orden:
```bash
curl -X PATCH http://127.0.0.1:8000/api/orders/1/ \
  -H "Content-Type: application/json" \
  -d '{"status": "shipped"}'
```

### Eliminar una reseña:
```bash
curl -X DELETE http://127.0.0.1:8000/api/reviews/1/
```

---

## 📊 Configuración de Archivos

| Archivo | Descripción |
|---------|-------------|
| `djangov2/models.py` | Definición de 5 modelos Django |
| `djangov2/serializers.py` | Serializers con validaciones integradas |
| `djangov2/views.py` | ViewSets para CRUD de todos los modelos |
| `djangov2/urls.py` | Rutas con DefaultRouter |
| `djangov2/tests.py` | Suite de 60+ tests unitarios |
| `progl1_ute202601/settings.py` | Configuración con rest_framework |
| `progl1_ute202601/urls.py` | URLs raíz incluye `/api/` |

---

## 🎯 Conclusiones

✅ **API completamente funcional** - Todos los CRUD operativos  
✅ **Validaciones robustas** - Prevención de datos inválidos  
✅ **Cobertura de tests** - 60+ tests automatizados  
✅ **Documentación completa** - Ejemplos de cada endpoint  
✅ **Manejo de errores** - Respuestas coherentes (200, 201, 400, 404)  
✅ **Extensible** - Fácil agregar autenticación, permisos, paginación  

---

**Última actualización:** 5 de Julio, 2026
