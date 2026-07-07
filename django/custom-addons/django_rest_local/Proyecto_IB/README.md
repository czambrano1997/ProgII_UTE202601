# API REST de Sistema de Gestión de Biblioteca - Django REST Framework

## 📋 Descripción del Proyecto

Este proyecto implementa una **API REST completa** utilizando Django REST Framework para un sistema de gestión de biblioteca. La API expone 5 modelos de datos con endpoints CRUD (GET, POST, PUT, PATCH, DELETE) completamente funcionales.

---

## 🏗️ Modelos Implementados

### 1. **Autor**
Gestión de autores de libros.

**Campos:**
- `id`: Identificador único (auto-generado)
- `nombre`: Nombre del autor (CharField, max_length=100)
- `apellido`: Apellido del autor (CharField, max_length=100)
- `fecha_nacimiento`: Fecha de nacimiento (DateField, nullable)

**Relaciones:** Uno-a-Muchos con Libro

---

### 2. **Editorial**
Gestión de editoriales que publican libros.

**Campos:**
- `id`: Identificador único (auto-generado)
- `nombre`: Nombre de la editorial (CharField, max_length=100)
- `pais`: País de origen (CharField, max_length=50, default='España')

**Relaciones:** Uno-a-Muchos con Libro

---

### 3. **Categoria**
Clasificación de libros por género o tipo.

**Campos:**
- `id`: Identificador único (auto-generado)
- `nombre`: Nombre de la categoría (CharField, max_length=100)
- `descripcion`: Descripción de la categoría (TextField, nullable)

**Relaciones:** Uno-a-Muchos con Libro

---

### 4. **Libro**
Información detallada de libros en la biblioteca.

**Campos:**
- `id`: Identificador único (auto-generado)
- `titulo`: Título del libro (CharField, max_length=200)
- `autor`: Referencia a Autor (ForeignKey)
- `editorial`: Referencia a Editorial (ForeignKey)
- `categoria`: Referencia a Categoria (ForeignKey)
- `isbn`: Código ISBN único (CharField, max_length=13, unique=True)
- `fecha_publicacion`: Fecha de publicación (DateField)
- `paginas`: Número de páginas (IntegerField)

**Relaciones:** Muchos-a-Uno con Autor, Editorial, Categoria; Uno-a-Muchos con Prestamo

---

### 5. **Prestamo**
Registro de préstamos de libros.

**Campos:**
- `id`: Identificador único (auto-generado)
- `libro`: Referencia a Libro (ForeignKey)
- `usuario`: Nombre del usuario (CharField, max_length=100)
- `fecha_prestamo`: Fecha y hora del préstamo (DateTimeField, auto-generado)
- `fecha_devolucion_esperada`: Fecha esperada de devolución (DateField)
- `fecha_devolucion_real`: Fecha real de devolución (DateField, nullable)
- `estado`: Estado del préstamo (CharField, opciones: 'activo', 'devuelto', 'vencido')

**Relaciones:** Muchos-a-Uno con Libro

---

## 🔧 Configuraciones Realizadas

### 1. **Instalación de Dependencias**
```bash
pip install djangorestframework
```

### 2. **Actualización de settings.py**
Se agregaron las siguientes apps a `INSTALLED_APPS`:
```python
INSTALLED_APPS = [
    # ... apps de Django ...
    'rest_framework',
    'rest_framework.authtoken',
    'tienda',
]
```

### 3. **Creación de Migraciones**
```bash
python manage.py makemigrations
python manage.py migrate
```

Se creó la migración `0002_autor_categoria_editorial_libro_prestamo_and_more.py` que:
- Crea los 5 modelos nuevos
- Elimina el modelo Producto anterior

### 4. **Estructura de Archivos Modificados**

```
tienda/
├── models.py          # 5 modelos de datos
├── serializers.py     # 5 serializadores (validación y serialización)
├── views.py           # 5 ViewSets con lógica de negocio
├── urls.py            # Configuración de rutas con DefaultRouter
├── admin.py           # Registro de modelos en admin de Django
└── migrations/
    ├── 0001_initial.py
    └── 0002_autor_categoria_editorial_libro_prestamo_and_more.py
```

---

## 🚀 Endpoints de la API

### Base URL
```
http://localhost:8000/api/
```

---

## 📖 Métodos HTTP Implementados

### **AUTORES** - `/api/autores/`

#### GET - Obtener todos los autores
```http
GET /api/autores/
```
**Response:**
```json
[
    {
        "id": 1,
        "nombre": "Gabriel",
        "apellido": "García Márquez",
        "fecha_nacimiento": "1927-03-06"
    }
]
```

#### POST - Crear un nuevo autor
```http
POST /api/autores/
Content-Type: application/json

{
    "nombre": "Gabriel",
    "apellido": "García Márquez",
    "fecha_nacimiento": "1927-03-06"
}
```
**Response:** Status 201 Created
```json
{
    "id": 1,
    "nombre": "Gabriel",
    "apellido": "García Márquez",
    "fecha_nacimiento": "1927-03-06"
}
```

#### GET - Obtener un autor específico
```http
GET /api/autores/1/
```
**Response:**
```json
{
    "id": 1,
    "nombre": "Gabriel",
    "apellido": "García Márquez",
    "fecha_nacimiento": "1927-03-06"
}
```

#### PUT - Actualizar completamente un autor
```http
PUT /api/autores/1/
Content-Type: application/json

{
    "nombre": "Gabriel",
    "apellido": "García Márquez",
    "fecha_nacimiento": "1927-03-07"
}
```
**Response:** Status 200 OK

#### PATCH - Actualizar parcialmente un autor
```http
PATCH /api/autores/1/
Content-Type: application/json

{
    "nombre": "Gabriel José"
}
```
**Response:** Status 200 OK
```json
{
    "id": 1,
    "nombre": "Gabriel José",
    "apellido": "García Márquez",
    "fecha_nacimiento": "1927-03-06"
}
```

#### DELETE - Eliminar un autor
```http
DELETE /api/autores/1/
```
**Response:** Status 204 No Content

---

### **EDITORIALES** - `/api/editoriales/`

#### GET - Obtener todas las editoriales
```http
GET /api/editoriales/
```

#### POST - Crear una nueva editorial
```http
POST /api/editoriales/
Content-Type: application/json

{
    "nombre": "Sudamericana",
    "pais": "Argentina"
}
```

#### GET - Obtener una editorial específica
```http
GET /api/editoriales/1/
```

#### PUT - Actualizar completamente una editorial
```http
PUT /api/editoriales/1/
Content-Type: application/json

{
    "nombre": "Sudamericana Editorial",
    "pais": "Argentina"
}
```

#### PATCH - Actualizar parcialmente una editorial
```http
PATCH /api/editoriales/1/
Content-Type: application/json

{
    "pais": "Uruguay"
}
```

#### DELETE - Eliminar una editorial
```http
DELETE /api/editoriales/1/
```

---

### **CATEGORÍAS** - `/api/categorias/`

#### GET - Obtener todas las categorías
```http
GET /api/categorias/
```

#### POST - Crear una nueva categoría
```http
POST /api/categorias/
Content-Type: application/json

{
    "nombre": "Ficción",
    "descripcion": "Novelas de ficción literaria"
}
```

#### GET - Obtener una categoría específica
```http
GET /api/categorias/1/
```

#### PUT - Actualizar completamente una categoría
```http
PUT /api/categorias/1/
Content-Type: application/json

{
    "nombre": "Ficción Contemporánea",
    "descripcion": "Novelas de ficción contemporánea"
}
```

#### PATCH - Actualizar parcialmente una categoría
```http
PATCH /api/categorias/1/
Content-Type: application/json

{
    "descripcion": "Novelas clásicas de ficción"
}
```

#### DELETE - Eliminar una categoría
```http
DELETE /api/categorias/1/
```

---

### **LIBROS** - `/api/libros/`

#### GET - Obtener todos los libros
```http
GET /api/libros/
```
**Response:**
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

#### POST - Crear un nuevo libro
```http
POST /api/libros/
Content-Type: application/json

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
**Response:** Status 201 Created

#### GET - Obtener un libro específico
```http
GET /api/libros/1/
```

#### PUT - Actualizar completamente un libro
```http
PUT /api/libros/1/
Content-Type: application/json

{
    "titulo": "Cien años de soledad",
    "autor": 1,
    "editorial": 1,
    "categoria": 1,
    "isbn": "9788467033502",
    "fecha_publicacion": "1967-05-30",
    "paginas": 472
}
```

#### PATCH - Actualizar parcialmente un libro
```http
PATCH /api/libros/1/
Content-Type: application/json

{
    "paginas": 471
}
```

#### DELETE - Eliminar un libro
```http
DELETE /api/libros/1/
```

#### GET - Filtrar libros por categoría (Endpoint personalizado)
```http
GET /api/libros/por_categoria/?categoria_id=1
```
**Response:**
```json
[
    {
        "id": 1,
        "titulo": "Cien años de soledad",
        ...
    }
]
```

---

### **PRÉSTAMOS** - `/api/prestamos/`

#### GET - Obtener todos los préstamos
```http
GET /api/prestamos/
```
**Response:**
```json
[
    {
        "id": 1,
        "libro": 1,
        "libro_titulo": "Cien años de soledad",
        "usuario": "Juan Pérez",
        "fecha_prestamo": "2025-01-15T10:30:00Z",
        "fecha_devolucion_esperada": "2025-01-29",
        "fecha_devolucion_real": null,
        "estado": "activo"
    }
]
```

#### POST - Crear un nuevo préstamo
```http
POST /api/prestamos/
Content-Type: application/json

{
    "libro": 1,
    "usuario": "Juan Pérez",
    "fecha_devolucion_esperada": "2025-01-29",
    "estado": "activo"
}
```
**Response:** Status 201 Created

#### GET - Obtener un préstamo específico
```http
GET /api/prestamos/1/
```

#### PUT - Actualizar completamente un préstamo
```http
PUT /api/prestamos/1/
Content-Type: application/json

{
    "libro": 1,
    "usuario": "Juan Pérez",
    "fecha_devolucion_esperada": "2025-02-05",
    "fecha_devolucion_real": "2025-01-29",
    "estado": "devuelto"
}
```

#### PATCH - Actualizar parcialmente un préstamo
```http
PATCH /api/prestamos/1/
Content-Type: application/json

{
    "estado": "devuelto",
    "fecha_devolucion_real": "2025-01-29"
}
```

#### DELETE - Eliminar un préstamo
```http
DELETE /api/prestamos/1/
```

#### GET - Obtener préstamos activos (Endpoint personalizado)
```http
GET /api/prestamos/activos/
```
**Response:**
```json
[
    {
        "id": 1,
        "libro": 1,
        "libro_titulo": "Cien años de soledad",
        "usuario": "Juan Pérez",
        "fecha_prestamo": "2025-01-15T10:30:00Z",
        "fecha_devolucion_esperada": "2025-01-29",
        "fecha_devolucion_real": null,
        "estado": "activo"
    }
]
```

---

## 🔐 Autenticación y Permisos

Se utilizó **IsAuthenticatedOrReadOnly** para todos los ViewSets:
- ✅ **GET**: Disponible para usuarios anónimos
- ✅ **POST, PUT, PATCH, DELETE**: Requerida autenticación

Para obtener un token de autenticación:
```bash
curl -X POST http://localhost:8000/api-token-auth/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "contraseña"}'
```

Usar el token en requests autenticados:
```bash
curl -X POST http://localhost:8000/api/autores/ \
  -H "Authorization: Token <tu_token>" \
  -H "Content-Type: application/json" \
  -d '{"nombre": "...}'
```

---

## 📝 Validaciones Implementadas

### Serializers con Validaciones Personalizadas

**LibroSerializer:**
- ✓ Validación que el número de páginas sea > 0

**RelacionesPobladas:**
- ✓ Los serializers incluyen campos relacionados (read-only) para una mejor legibilidad

**ForeignKey Validations:**
- ✓ Django valida automáticamente que los IDs referenciados existan

---

## 🧪 Pruebas de la API

### Usando cURL

**Crear un autor:**
```bash
curl -X POST http://localhost:8000/api/autores/ \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Jorge Luis",
    "apellido": "Borges",
    "fecha_nacimiento": "1899-08-24"
  }'
```

**Obtener todos los autores:**
```bash
curl http://localhost:8000/api/autores/
```

**Actualizar un autor (PATCH):**
```bash
curl -X PATCH http://localhost:8000/api/autores/1/ \
  -H "Content-Type: application/json" \
  -d '{"nombre": "Jorge Luis José"}'
```

**Eliminar un autor:**
```bash
curl -X DELETE http://localhost:8000/api/autores/1/
```

### Usando Postman o Insomnia
1. Importar collection desde: `http://localhost:8000/api/`
2. La interfaz Browsable de DRF permite probar todos los endpoints

---

## 🔍 Visualización en Navegador

Django REST Framework proporciona una interfaz web interactiva:

- `http://localhost:8000/api/` - API Root
- `http://localhost:8000/api/autores/` - Formulario HTML para crear/editar autores
- `http://localhost:8000/api/editoriales/` - Formulario HTML para editoriales
- `http://localhost:8000/api/categorias/` - Formulario HTML para categorías
- `http://localhost:8000/api/libros/` - Formulario HTML para libros
- `http://localhost:8000/api/prestamos/` - Formulario HTML para préstamos

---

## 📊 Estructura de Respuestas

### Formato de Pagina (Listados)
```json
{
    "count": 10,
    "next": "http://localhost:8000/api/autores/?page=2",
    "previous": null,
    "results": [...]
}
```

### Códigos HTTP Utilizados
| Método | Status | Descripción |
|--------|--------|-------------|
| GET | 200 | OK - Recurso obtenido |
| POST | 201 | Created - Recurso creado |
| PUT | 200 | OK - Recurso actualizado completamente |
| PATCH | 200 | OK - Recurso actualizado parcialmente |
| DELETE | 204 | No Content - Recurso eliminado |
| 400 | Bad Request - Error de validación |
| 404 | Not Found - Recurso no encontrado |

---

## 🎯 Conclusiones

### ✅ Logros Alcanzados

1. **Implementación Completa de CRUD**
   - 5 modelos con endpoints CRUD completos
   - Todas las operaciones (GET, POST, PUT, PATCH, DELETE) funcionan correctamente

2. **Arquitectura RESTful**
   - Uso de viewsets y routers automáticos
   - Siguiendo convenciones estándar REST
   - URLs intuitivas y consistentes

3. **Validaciones y Integridad**
   - Validaciones de datos en serializers
   - Relaciones entre modelos correctamente establecidas
   - Validaciones automáticas de Django

4. **Autenticación y Permisos**
   - Implementación de permisos IsAuthenticatedOrReadOnly
   - Protección de operaciones sensibles

5. **Endpoints Personalizados**
   - Filtros avanzados (libros por categoría, préstamos activos)
   - Extensibilidad para futuras funcionalidades

### 🔮 Mejoras Futuras

- [ ] Implementar filtrado avanzado con django-filter
- [ ] Agregar paginación configurable
- [ ] Implementar búsqueda full-text
- [ ] Agregar ordenamiento dinámico
- [ ] Tests unitarios e integración
- [ ] Documentación automática con Swagger/OpenAPI
- [ ] Rate limiting para proteger la API
- [ ] Caching con Redis

### 📚 Tecnologías Utilizadas

- **Django 6.0.6** - Framework web
- **Django REST Framework 3.17.1** - API REST
- **Python 3.13** - Lenguaje de programación
- **SQLite3** - Base de datos

---

## 🚀 Ejecución del Servidor

```bash
python manage.py runserver
```

El servidor estará disponible en: `http://localhost:8000`

---

## 📄 Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

---

**Autor:** Proyecto ProgII - UTE 2026-01  
**Fecha:** 2025-01-15  
**Versión:** 1.0.0
