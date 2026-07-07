# 🔍 Documentación de Métodos HTTP - API REST Django

## Resumen Ejecutivo

Este documento detalla la implementación de todos los métodos HTTP (GET, POST, PUT, PATCH, DELETE) para los 5 modelos del sistema de gestión de biblioteca.

---

## 📊 Tabla Comparativa de Métodos HTTP

| Método | Operación | Idempotente | Seguro | Caso de Uso |
|--------|-----------|------------|--------|-----------|
| **GET** | Lectura | ✓ Sí | ✓ Sí | Obtener recurso(s) |
| **POST** | Creación | ✗ No | ✗ No | Crear nuevo recurso |
| **PUT** | Actualización Total | ✓ Sí | ✗ No | Reemplazar recurso completo |
| **PATCH** | Actualización Parcial | ✗ No | ✗ No | Actualizar algunos campos |
| **DELETE** | Eliminación | ✓ Sí | ✗ No | Eliminar recurso |

---

## 🔴 GET - Método de Lectura

### Características
- **Propósito:** Obtener datos sin modificar el servidor
- **Idempotente:** Sí (múltiples llamadas = mismo resultado)
- **Seguro:** Sí (no modifica datos)
- **Requiere Autenticación:** No (IsAuthenticatedOrReadOnly)
- **Cuerpo de Solicitud:** No
- **Códigos de Respuesta:** 200 OK, 404 Not Found

### Variantes de GET

#### GET /api/autores/ - Listar todos
```http
GET /api/autores/ HTTP/1.1
Host: localhost:8000
Accept: application/json
```

**Respuesta 200 OK:**
```json
{
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "nombre": "Gabriel",
            "apellido": "García Márquez",
            "fecha_nacimiento": "1927-03-06"
        },
        {
            "id": 2,
            "nombre": "Jorge Luis",
            "apellido": "Borges",
            "fecha_nacimiento": "1899-08-24"
        }
    ]
}
```

#### GET /api/autores/1/ - Obtener por ID
```http
GET /api/autores/1/ HTTP/1.1
Host: localhost:8000
Accept: application/json
```

**Respuesta 200 OK:**
```json
{
    "id": 1,
    "nombre": "Gabriel",
    "apellido": "García Márquez",
    "fecha_nacimiento": "1927-03-06"
}
```

**Respuesta 404 Not Found (ID no existe):**
```json
{
    "detail": "Not found."
}
```

#### GET /api/libros/por_categoria/?categoria_id=1 - Filtro personalizado
```http
GET /api/libros/por_categoria/?categoria_id=1 HTTP/1.1
Host: localhost:8000
Accept: application/json
```

**Respuesta 200 OK:**
```json
[
    {
        "id": 1,
        "titulo": "Cien años de soledad",
        "autor": 1,
        "autor_nombre": "Gabriel",
        "editorial": 1,
        "editorial_nombre": "Sudamericana",
        "categoria": 1,
        "categoria_nombre": "Ficción",
        "isbn": "9788467033502",
        "fecha_publicacion": "1967-05-30",
        "paginas": 471
    }
]
```

**Respuesta 400 Bad Request (parámetro faltante):**
```json
{
    "error": "categoria_id es requerido"
}
```

---

## 🟢 POST - Método de Creación

### Características
- **Propósito:** Crear un nuevo recurso
- **Idempotente:** No (cada llamada crea un nuevo recurso)
- **Seguro:** No (modifica el servidor)
- **Requiere Autenticación:** Sí
- **Cuerpo de Solicitud:** JSON con datos del recurso
- **Códigos de Respuesta:** 201 Created, 400 Bad Request, 401 Unauthorized

### Flujo de POST

#### POST /api/autores/ - Crear autor
```http
POST /api/autores/ HTTP/1.1
Host: localhost:8000
Content-Type: application/json
Authorization: Token abc123def456

{
    "nombre": "Gabriel",
    "apellido": "García Márquez",
    "fecha_nacimiento": "1927-03-06"
}
```

**Respuesta 201 Created:**
```json
{
    "id": 1,
    "nombre": "Gabriel",
    "apellido": "García Márquez",
    "fecha_nacimiento": "1927-03-06"
}
```

**Headers de Respuesta:**
```
HTTP/1.1 201 Created
Location: /api/autores/1/
Content-Type: application/json
```

#### POST /api/libros/ - Crear libro
```http
POST /api/libros/ HTTP/1.1
Host: localhost:8000
Content-Type: application/json
Authorization: Token abc123def456

{
    "titulo": "Cien años de soledad",
    "autor": 1,
    "editorial": 1,
    "categoria": 1,
    "isbn": "9788467033502",
    "fecha_publicacion": "1967-05-30",
    "paginas": 471
}
```

**Respuesta 201 Created:**
```json
{
    "id": 1,
    "titulo": "Cien años de soledad",
    "autor": 1,
    "autor_nombre": "Gabriel",
    "editorial": 1,
    "editorial_nombre": "Sudamericana",
    "categoria": 1,
    "categoria_nombre": "Ficción",
    "isbn": "9788467033502",
    "fecha_publicacion": "1967-05-30",
    "paginas": 471
}
```

#### Errores en POST

**400 Bad Request - Datos incompletos:**
```json
{
    "titulo": ["This field is required."],
    "autor": ["This field is required."]
}
```

**400 Bad Request - Validación personalizada:**
```json
{
    "paginas": ["Las páginas deben ser mayor que 0"]
}
```

**400 Bad Request - Foreign Key inválido:**
```json
{
    "autor": ["Invalid pk \"999\" - object does not exist."]
}
```

**401 Unauthorized - Sin token:**
```json
{
    "detail": "Authentication credentials were not provided."
}
```

---

## 🔵 PUT - Método de Actualización Total

### Características
- **Propósito:** Reemplazar completamente un recurso
- **Idempotente:** Sí (múltiples llamadas = mismo resultado)
- **Seguro:** No (modifica el servidor)
- **Requiere Autenticación:** Sí
- **Cuerpo de Solicitud:** JSON con TODOS los campos
- **Diferencia con PATCH:** PUT requiere todos los campos, PATCH solo los que cambien
- **Códigos de Respuesta:** 200 OK, 400 Bad Request, 401 Unauthorized, 404 Not Found

### Flujo de PUT

#### PUT /api/autores/1/ - Actualizar completamente
```http
PUT /api/autores/1/ HTTP/1.1
Host: localhost:8000
Content-Type: application/json
Authorization: Token abc123def456

{
    "nombre": "Gabriel José",
    "apellido": "García Márquez",
    "fecha_nacimiento": "1927-03-06"
}
```

**Respuesta 200 OK:**
```json
{
    "id": 1,
    "nombre": "Gabriel José",
    "apellido": "García Márquez",
    "fecha_nacimiento": "1927-03-06"
}
```

#### Ejemplos de Errores en PUT

**400 Bad Request - Campo incompleto:**
```http
PUT /api/autores/1/ HTTP/1.1
Host: localhost:8000
Content-Type: application/json
Authorization: Token abc123def456

{
    "nombre": "Gabriel José"
}
```

**Respuesta:**
```json
{
    "apellido": ["This field is required."],
    "fecha_nacimiento": ["This field is required."]
}
```

**404 Not Found - ID inexistente:**
```http
PUT /api/autores/999/ HTTP/1.1
```

**Respuesta:**
```json
{
    "detail": "Not found."
}
```

---

## 🟡 PATCH - Método de Actualización Parcial

### Características
- **Propósito:** Actualizar solo algunos campos
- **Idempotente:** No (última modificación gana)
- **Seguro:** No (modifica el servidor)
- **Requiere Autenticación:** Sí
- **Cuerpo de Solicitud:** JSON con solo los campos a cambiar
- **Ventaja sobre PUT:** Menor ancho de banda, más flexible
- **Códigos de Respuesta:** 200 OK, 400 Bad Request, 401 Unauthorized, 404 Not Found

### Flujo de PATCH

#### PATCH /api/autores/1/ - Actualizar parcialmente
```http
PATCH /api/autores/1/ HTTP/1.1
Host: localhost:8000
Content-Type: application/json
Authorization: Token abc123def456

{
    "nombre": "Gabriel Newname"
}
```

**Respuesta 200 OK:**
```json
{
    "id": 1,
    "nombre": "Gabriel Newname",
    "apellido": "García Márquez",
    "fecha_nacimiento": "1927-03-06"
}
```

#### PATCH /api/prestamos/1/ - Marcar como devuelto
```http
PATCH /api/prestamos/1/ HTTP/1.1
Host: localhost:8000
Content-Type: application/json
Authorization: Token abc123def456

{
    "estado": "devuelto",
    "fecha_devolucion_real": "2025-01-25"
}
```

**Respuesta 200 OK:**
```json
{
    "id": 1,
    "libro": 1,
    "libro_titulo": "Cien años de soledad",
    "usuario": "Juan Pérez",
    "fecha_prestamo": "2025-01-15T10:30:00Z",
    "fecha_devolucion_esperada": "2025-01-29",
    "fecha_devolucion_real": "2025-01-25",
    "estado": "devuelto"
}
```

#### Comparación: PUT vs PATCH

```
Escenario: Cambiar solo el nombre de un autor

╔═════════════════════════╦═════════════════════════╗
║        PUT              ║       PATCH             ║
╠═════════════════════════╬═════════════════════════╣
║ Requiere todos campos   ║ Solo campos a cambiar   ║
║ ✓ Más predecible        ║ ✓ Menos ancho de banda  ║
║ ✗ Más datos enviados    ║ ✗ Menos predecible      ║
║                         ║                         ║
║ {                       ║ {                       ║
║   "nombre": "Gabriel",  ║   "nombre": "Gabriel"   ║
║   "apellido": "García", ║ }                       ║
║   "fecha_nac": "1927"   ║                         ║
║ }                       ║                         ║
╚═════════════════════════╩═════════════════════════╝
```

---

## 🔴 DELETE - Método de Eliminación

### Características
- **Propósito:** Eliminar un recurso
- **Idempotente:** Sí (múltiples llamadas = mismo resultado)
- **Seguro:** No (modifica el servidor)
- **Requiere Autenticación:** Sí
- **Cuerpo de Solicitud:** No
- **Códigos de Respuesta:** 204 No Content, 401 Unauthorized, 404 Not Found

### Flujo de DELETE

#### DELETE /api/autores/1/ - Eliminar autor
```http
DELETE /api/autores/1/ HTTP/1.1
Host: localhost:8000
Authorization: Token abc123def456
```

**Respuesta 204 No Content:**
```
(Sin cuerpo de respuesta)
```

#### DELETE /api/libros/1/ - Eliminar libro
```http
DELETE /api/libros/1/ HTTP/1.1
Host: localhost:8000
Authorization: Token abc123def456
```

**Respuesta 204 No Content:**
```
(Sin cuerpo de respuesta)
```

#### Errores en DELETE

**404 Not Found - ID no existe:**
```http
DELETE /api/autores/999/ HTTP/1.1
```

**Respuesta:**
```json
{
    "detail": "Not found."
}
```

**401 Unauthorized - Sin autenticación:**
```http
DELETE /api/autores/1/ HTTP/1.1
```

**Respuesta:**
```json
{
    "detail": "Authentication credentials were not provided."
}
```

---

## 🔐 Autenticación y Autorización

### Obtener Token
```http
POST /api-token-auth/ HTTP/1.1
Host: localhost:8000
Content-Type: application/json

{
    "username": "admin",
    "password": "contraseña"
}
```

**Respuesta 200 OK:**
```json
{
    "token": "abc123def456..."
}
```

### Usar Token en Requests
```http
GET /api/autores/ HTTP/1.1
Host: localhost:8000
Authorization: Token abc123def456...
```

---

## 📈 Códigos de Estado HTTP

| Código | Nombre | Descripción | Ejemplo |
|--------|--------|-------------|---------|
| **200** | OK | Solicitud exitosa | GET, PUT, PATCH |
| **201** | Created | Recurso creado exitosamente | POST |
| **204** | No Content | Solicitud exitosa sin contenido | DELETE |
| **400** | Bad Request | Datos inválidos en la solicitud | Validación fallida |
| **401** | Unauthorized | Autenticación requerida | Token faltante |
| **403** | Forbidden | Permiso denegado | Usuario sin permiso |
| **404** | Not Found | Recurso no encontrado | ID inválido |
| **500** | Server Error | Error interno del servidor | Excepción no manejada |

---

## 🧪 Ejemplos Prácticos Completos

### Caso 1: Ciclo Completo de un Libro

```bash
# 1. Crear Autor (POST)
curl -X POST http://localhost:8000/api/autores/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token <token>" \
  -d '{"nombre":"Jorge Luis","apellido":"Borges","fecha_nacimiento":"1899-08-24"}'

# Response: {"id": 2, ...}

# 2. Crear Editorial (POST)
curl -X POST http://localhost:8000/api/editoriales/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token <token>" \
  -d '{"nombre":"Emecé","pais":"Argentina"}'

# Response: {"id": 2, ...}

# 3. Crear Categoría (POST)
curl -X POST http://localhost:8000/api/categorias/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token <token>" \
  -d '{"nombre":"Ensayo","descripcion":"Obras de ensayo"}'

# Response: {"id": 2, ...}

# 4. Crear Libro (POST)
curl -X POST http://localhost:8000/api/libros/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token <token>" \
  -d '{"titulo":"Ficciones","autor":2,"editorial":2,"categoria":2,"isbn":"9788435062809","fecha_publicacion":"1944-12-17","paginas":156}'

# Response: {"id": 2, "titulo": "Ficciones", ...}

# 5. Obtener Libro (GET)
curl http://localhost:8000/api/libros/2/

# 6. Actualizar páginas (PATCH)
curl -X PATCH http://localhost:8000/api/libros/2/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token <token>" \
  -d '{"paginas":160}'

# 7. Crear Préstamo (POST)
curl -X POST http://localhost:8000/api/prestamos/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token <token>" \
  -d '{"libro":2,"usuario":"María López","fecha_devolucion_esperada":"2025-02-05","estado":"activo"}'

# 8. Obtener préstamos activos (GET con filtro)
curl http://localhost:8000/api/prestamos/activos/

# 9. Marcar como devuelto (PATCH)
curl -X PATCH http://localhost:8000/api/prestamos/1/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token <token>" \
  -d '{"estado":"devuelto","fecha_devolucion_real":"2025-01-28"}'

# 10. Eliminar autor antiguo (DELETE)
curl -X DELETE http://localhost:8000/api/autores/1/ \
  -H "Authorization: Token <token>"
```

---

## 📊 Matriz de Métodos HTTP por Modelo

| Endpoint | GET | POST | PUT | PATCH | DELETE |
|----------|-----|------|-----|-------|--------|
| `/api/autores/` | ✓ | ✓ | - | - | - |
| `/api/autores/{id}/` | ✓ | - | ✓ | ✓ | ✓ |
| `/api/editoriales/` | ✓ | ✓ | - | - | - |
| `/api/editoriales/{id}/` | ✓ | - | ✓ | ✓ | ✓ |
| `/api/categorias/` | ✓ | ✓ | - | - | - |
| `/api/categorias/{id}/` | ✓ | - | ✓ | ✓ | ✓ |
| `/api/libros/` | ✓ | ✓ | - | - | - |
| `/api/libros/{id}/` | ✓ | - | ✓ | ✓ | ✓ |
| `/api/libros/por_categoria/` | ✓ | - | - | - | - |
| `/api/prestamos/` | ✓ | ✓ | - | - | - |
| `/api/prestamos/{id}/` | ✓ | - | ✓ | ✓ | ✓ |
| `/api/prestamos/activos/` | ✓ | - | - | - | - |

---

## 🎯 Conclusiones sobre Métodos HTTP

### Buenas Prácticas Implementadas

1. ✅ **GET**: Solo lectura, sin autenticación requerida
2. ✅ **POST**: Crea nuevos recursos, requiere autenticación
3. ✅ **PUT/PATCH**: Actualización completa vs parcial diferenciada
4. ✅ **DELETE**: Elimina recursos, requiere autenticación
5. ✅ **Códigos HTTP**: Utilizados correctamente (200, 201, 204, 400, 404)
6. ✅ **Validaciones**: Errores descriptivos en respuestas
7. ✅ **Relaciones**: Foreign Keys validadas automáticamente

### Seguridad

- 🔒 **IsAuthenticatedOrReadOnly**: Acceso público para lectura
- 🔒 **Autenticación por Token**: Requerida para modificaciones
- 🔒 **Validaciones de Entrada**: Todo dato validado antes de guardar

---

**Autor:** Proyecto ProgII - UTE 2026-01  
**Versión:** 1.0.0  
**Fecha:** 2025-01-15
