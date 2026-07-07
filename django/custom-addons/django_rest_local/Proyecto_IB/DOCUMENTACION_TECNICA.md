# 📖 Documentación Técnica de Implementación - API REST Django

## 📑 Índice
1. [Instalación y Configuración](#instalación-y-configuración)
2. [Estructura de Modelos](#estructura-de-modelos)
3. [Serializers](#serializers)
4. [ViewSets](#viewsets)
5. [URLs y Routing](#urls-y-routing)
6. [Métodos HTTP Detallados](#métodos-http-detallados)
7. [Ejemplos de Uso](#ejemplos-de-uso)

---

## 🔧 Instalación y Configuración

### Paso 1: Instalar Django REST Framework
```bash
pip install djangorestframework
```

### Paso 2: Agregar a INSTALLED_APPS en settings.py
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',                # ✓ Agregado
    'rest_framework.authtoken',      # ✓ Agregado
    'tienda',
]
```

### Paso 3: Configurar Permisos en settings.py (Opcional)
```python
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}
```

---

## 🏗️ Estructura de Modelos

### Diagrama de Relaciones
```
┌─────────────────────────────────────────────────────┐
│                     LIBRO                           │
│  ┌────────────┬───────────────┬─────────────────┐  │
│  │ PK: id     │ isbn (UNIQUE) │ titulo          │  │
│  │ FK: autor  │ FK: editorial │ FK: categoria   │  │
│  │ paginas    │ fecha_pub     │                 │  │
│  └────────────┴───────────────┴─────────────────┘  │
│        ▲             ▲                ▲             │
│        │             │                │             │
│   ┌────┴─┐      ┌────┴────┐      ┌───┴──────┐     │
│   │      │      │         │      │          │     │
│  AUTOR EDITORIAL          │   CATEGORIA      │     │
│   ●      ●                │       ●          │     │
│   │      │                │       │          │     │
│   └──────┴────────────────┴───────┴──────────┘     │
│                                                     │
│                    PRESTAMO                         │
│             ┌──────────────────────┐               │
│             │ FK: libro            │               │
│             │ usuario              │               │
│             │ fecha_prestamo       │               │
│             │ fecha_dev_esperada   │               │
│             │ fecha_dev_real       │               │
│             │ estado               │               │
│             └──────────────────────┘               │
└─────────────────────────────────────────────────────┘
```

### Código de Modelos
```python
# tienda/models.py

class Autor(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class Editorial(models.Model):
    nombre = models.CharField(max_length=100)
    pais = models.CharField(max_length=50, default='España')
    
    def __str__(self):
        return self.nombre

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    
    def __str__(self):
        return self.nombre

class Libro(models.Model):
    titulo = models.CharField(max_length=200)
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE)
    editorial = models.ForeignKey(Editorial, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    isbn = models.CharField(max_length=13, unique=True)
    fecha_publicacion = models.DateField()
    paginas = models.IntegerField()
    
    def __str__(self):
        return self.titulo

class Prestamo(models.Model):
    ESTADO_CHOICES = [
        ('activo', 'Activo'),
        ('devuelto', 'Devuelto'),
        ('vencido', 'Vencido'),
    ]
    
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
    usuario = models.CharField(max_length=100)
    fecha_prestamo = models.DateTimeField(auto_now_add=True)
    fecha_devolucion_esperada = models.DateField()
    fecha_devolucion_real = models.DateField(null=True, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='activo')
    
    def __str__(self):
        return f"Préstamo de {self.libro} a {self.usuario}"
```

---

## 📦 Serializers

### ¿Qué es un Serializer?
Un serializer en Django REST Framework convierte objetos de modelo complejos en JSON y valida datos de entrada.

### Código de Serializers
```python
# tienda/serializers.py

class AutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Autor
        fields = ['id', 'nombre', 'apellido', 'fecha_nacimiento']

class EditorialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Editorial
        fields = ['id', 'nombre', 'pais']

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id', 'nombre', 'descripcion']

class LibroSerializer(serializers.ModelSerializer):
    # Campos read-only para mostrar nombres relacionados
    autor_nombre = serializers.CharField(source='autor.nombre', read_only=True)
    editorial_nombre = serializers.CharField(source='editorial.nombre', read_only=True)
    categoria_nombre = serializers.CharField(source='categoria.nombre', read_only=True)
    
    class Meta:
        model = Libro
        fields = ['id', 'titulo', 'autor', 'autor_nombre', 'editorial', 'editorial_nombre', 
                  'categoria', 'categoria_nombre', 'isbn', 'fecha_publicacion', 'paginas']
    
    def validate_paginas(self, value):
        if value <= 0:
            raise serializers.ValidationError("Las páginas deben ser mayor que 0")
        return value

class PrestamoSerializer(serializers.ModelSerializer):
    libro_titulo = serializers.CharField(source='libro.titulo', read_only=True)
    
    class Meta:
        model = Prestamo
        fields = ['id', 'libro', 'libro_titulo', 'usuario', 'fecha_prestamo', 
                  'fecha_devolucion_esperada', 'fecha_devolucion_real', 'estado']
```

### Características de los Serializers

**AutorSerializer:**
- ✓ Serializa todos los campos del modelo Autor
- ✓ Incluye validación automática de tipos
- ✓ ID generado automáticamente

**LibroSerializer:**
- ✓ Incluye campos relacionados read-only (autor_nombre, editorial_nombre, etc.)
- ✓ Validación personalizada para el campo paginas
- ✓ Soporta nested relationships

**PrestamoSerializer:**
- ✓ Incluye título del libro como referencia legible
- ✓ Mantiene el ID del libro para operaciones de escritura

---

## 🎯 ViewSets

### ¿Qué es un ViewSet?
Un ViewSet es una vista que automatiza los 7 métodos HTTP comunes (list, create, retrieve, update, partial_update, destroy).

### Código de ViewSets
```python
# tienda/views.py

class AutorViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar Autores.
    Proporciona endpoints CRUD completos.
    """
    queryset = Autor.objects.all()
    serializer_class = AutorSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class EditorialViewSet(viewsets.ModelViewSet):
    queryset = Editorial.objects.all()
    serializer_class = EditorialSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class LibroViewSet(viewsets.ModelViewSet):
    queryset = Libro.objects.all()
    serializer_class = LibroSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    @action(detail=False, methods=['get'])
    def por_categoria(self, request):
        """Endpoint personalizado para obtener libros por categoría"""
        categoria_id = request.query_params.get('categoria_id')
        if not categoria_id:
            return Response({'error': 'categoria_id es requerido'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        libros = Libro.objects.filter(categoria_id=categoria_id)
        serializer = self.get_serializer(libros, many=True)
        return Response(serializer.data)

class PrestamoViewSet(viewsets.ModelViewSet):
    queryset = Prestamo.objects.all()
    serializer_class = PrestamoSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    @action(detail=False, methods=['get'])
    def activos(self, request):
        """Endpoint personalizado para obtener préstamos activos"""
        prestamos_activos = Prestamo.objects.filter(estado='activo')
        serializer = self.get_serializer(prestamos_activos, many=True)
        return Response(serializer.data)
```

### Métodos Automáticos del ModelViewSet

| Método | HTTP | Endpoint | Descripción |
|--------|------|----------|-------------|
| `list()` | GET | `/api/autores/` | Lista todos los recursos |
| `create()` | POST | `/api/autores/` | Crea un nuevo recurso |
| `retrieve()` | GET | `/api/autores/{id}/` | Obtiene un recurso específico |
| `update()` | PUT | `/api/autores/{id}/` | Actualiza completamente |
| `partial_update()` | PATCH | `/api/autores/{id}/` | Actualiza parcialmente |
| `destroy()` | DELETE | `/api/autores/{id}/` | Elimina un recurso |

### Acciones Personalizadas
```python
@action(detail=False, methods=['get'])  # detail=False: actúa sobre la colección
def por_categoria(self, request):
    # Implementación personalizada
    pass

@action(detail=True, methods=['post'])  # detail=True: actúa sobre un recurso específico
def marcar_devuelto(self, request, pk=None):
    # Implementación personalizada
    pass
```

---

## 🔗 URLs y Routing

### ¿Qué es DefaultRouter?
DefaultRouter es una utilidad que genera automáticamente todas las URLs REST a partir de los ViewSets registrados.

### Código de URLs
```python
# tienda/urls.py

from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import (AutorViewSet, EditorialViewSet, CategoriaViewSet, 
                    LibroViewSet, PrestamoViewSet)

router = DefaultRouter()
router.register(r'autores', AutorViewSet, basename='autor')
router.register(r'editoriales', EditorialViewSet, basename='editorial')
router.register(r'categorias', CategoriaViewSet, basename='categoria')
router.register(r'libros', LibroViewSet, basename='libro')
router.register(r'prestamos', PrestamoViewSet, basename='prestamo')

urlpatterns = [path('api/', include(router.urls))]
```

### URLs Generadas Automáticamente

```
GET    /api/
GET    /api/autores/
POST   /api/autores/
GET    /api/autores/{id}/
PUT    /api/autores/{id}/
PATCH  /api/autores/{id}/
DELETE /api/autores/{id}/

GET    /api/editoriales/
POST   /api/editoriales/
GET    /api/editoriales/{id}/
PUT    /api/editoriales/{id}/
PATCH  /api/editoriales/{id}/
DELETE /api/editoriales/{id}/

GET    /api/categorias/
POST   /api/categorias/
GET    /api/categorias/{id}/
PUT    /api/categorias/{id}/
PATCH  /api/categorias/{id}/
DELETE /api/categorias/{id}/

GET    /api/libros/
POST   /api/libros/
GET    /api/libros/{id}/
PUT    /api/libros/{id}/
PATCH  /api/libros/{id}/
DELETE /api/libros/{id}/
GET    /api/libros/por_categoria/?categoria_id={id}/

GET    /api/prestamos/
POST   /api/prestamos/
GET    /api/prestamos/{id}/
PUT    /api/prestamos/{id}/
PATCH  /api/prestamos/{id}/
DELETE /api/prestamos/{id}/
GET    /api/prestamos/activos/
```

---

## 🔄 Métodos HTTP Detallados

### GET - Obtener Recursos (Lectura)

#### GET /api/autores/ - Lista todos
```
REQUEST:
GET /api/autores/

RESPONSE (200 OK):
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
        }
    ]
}
```

#### GET /api/autores/1/ - Obtener uno específico
```
REQUEST:
GET /api/autores/1/

RESPONSE (200 OK):
{
    "id": 1,
    "nombre": "Gabriel",
    "apellido": "García Márquez",
    "fecha_nacimiento": "1927-03-06"
}
```

---

### POST - Crear Recursos (Crear)

#### POST /api/autores/
```
REQUEST:
POST /api/autores/
Content-Type: application/json

{
    "nombre": "Gabriel",
    "apellido": "García Márquez",
    "fecha_nacimiento": "1927-03-06"
}

RESPONSE (201 CREATED):
{
    "id": 1,
    "nombre": "Gabriel",
    "apellido": "García Márquez",
    "fecha_nacimiento": "1927-03-06"
}

Headers:
Location: /api/autores/1/
```

---

### PUT - Actualizar Completamente (Actualizar Total)

#### PUT /api/autores/1/
```
REQUEST:
PUT /api/autores/1/
Content-Type: application/json

{
    "nombre": "Gabriel José",
    "apellido": "García Márquez Updated",
    "fecha_nacimiento": "1927-03-07"
}

RESPONSE (200 OK):
{
    "id": 1,
    "nombre": "Gabriel José",
    "apellido": "García Márquez Updated",
    "fecha_nacimiento": "1927-03-07"
}

DIFERENCIA CON PATCH:
- PUT requiere TODOS los campos
- PATCH actualiza solo los campos proporcionados
```

---

### PATCH - Actualizar Parcialmente (Actualizar Parcial)

#### PATCH /api/autores/1/
```
REQUEST:
PATCH /api/autores/1/
Content-Type: application/json

{
    "nombre": "Gabriel Newname"
}

RESPONSE (200 OK):
{
    "id": 1,
    "nombre": "Gabriel Newname",
    "apellido": "García Márquez",
    "fecha_nacimiento": "1927-03-06"
}

VENTAJAS:
- Solo actualiza lo que envías
- Los campos no incluidos mantienen su valor
- Menor ancho de banda
```

---

### DELETE - Eliminar Recursos (Eliminar)

#### DELETE /api/autores/1/
```
REQUEST:
DELETE /api/autores/1/

RESPONSE (204 NO CONTENT):
(Sin cuerpo de respuesta)

Status: 204 No Content
```

---

## 💡 Ejemplos de Uso

### Ejemplo 1: Crear una Cadena Completa Libro → Autor → Editorial → Categoria → Prestamo

```bash
# 1. Crear Autor
curl -X POST http://localhost:8000/api/autores/ \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Gabriel",
    "apellido": "García Márquez",
    "fecha_nacimiento": "1927-03-06"
  }'
# Response: {"id": 1, ...}

# 2. Crear Editorial
curl -X POST http://localhost:8000/api/editoriales/ \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Sudamericana",
    "pais": "Argentina"
  }'
# Response: {"id": 1, ...}

# 3. Crear Categoría
curl -X POST http://localhost:8000/api/categorias/ \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Ficción Latinoamericana",
    "descripcion": "Novelas de autores latinoamericanos"
  }'
# Response: {"id": 1, ...}

# 4. Crear Libro (referenciando Autor, Editorial, Categoria)
curl -X POST http://localhost:8000/api/libros/ \
  -H "Content-Type: application/json" \
  -d '{
    "titulo": "Cien años de soledad",
    "autor": 1,
    "editorial": 1,
    "categoria": 1,
    "isbn": "9788467033502",
    "fecha_publicacion": "1967-05-30",
    "paginas": 471
  }'
# Response: {"id": 1, "titulo": "Cien años de soledad", ...}

# 5. Crear Préstamo
curl -X POST http://localhost:8000/api/prestamos/ \
  -H "Content-Type: application/json" \
  -d '{
    "libro": 1,
    "usuario": "Juan Pérez",
    "fecha_devolucion_esperada": "2025-01-29",
    "estado": "activo"
  }'
# Response: {"id": 1, "libro": 1, "usuario": "Juan Pérez", ...}
```

### Ejemplo 2: Flujo de Devolución de Libro

```bash
# 1. Obtener préstamo activo
curl http://localhost:8000/api/prestamos/1/

# 2. Actualizar estado a "devuelto" con fecha real
curl -X PATCH http://localhost:8000/api/prestamos/1/ \
  -H "Content-Type: application/json" \
  -d '{
    "estado": "devuelto",
    "fecha_devolucion_real": "2025-01-25"
  }'

# Response: {"id": 1, "estado": "devuelto", "fecha_devolucion_real": "2025-01-25", ...}
```

### Ejemplo 3: Filtrar Libros por Categoría

```bash
# Obtener libros de la categoría 1
curl "http://localhost:8000/api/libros/por_categoria/?categoria_id=1"

# Response: [{"id": 1, "titulo": "Cien años de soledad", ...}]
```

### Ejemplo 4: Obtener Préstamos Activos

```bash
curl http://localhost:8000/api/prestamos/activos/

# Response:
[
  {
    "id": 1,
    "libro": 1,
    "usuario": "Juan Pérez",
    "estado": "activo",
    ...
  }
]
```

---

## 🛠️ Migración de Datos

```bash
# Crear nueva migración
python manage.py makemigrations

# Ver migraciones pendientes
python manage.py showmigrations

# Aplicar migraciones
python manage.py migrate

# Ver cambios SQL sin aplicar
python manage.py sqlmigrate tienda 0002
```

---

## 🔍 Debugging

### Ver QuerySet SQL
```python
from tienda.models import Libro
print(Libro.objects.all().query)
```

### Habilitar Logging
```python
# En settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',
    },
}
```

---

## 📋 Checklist de Implementación

- ✅ Instalar Django REST Framework
- ✅ Agregar a INSTALLED_APPS
- ✅ Crear 5 modelos con relaciones ForeignKey
- ✅ Crear serializers para cada modelo
- ✅ Crear viewsets para cada modelo
- ✅ Configurar URLs con DefaultRouter
- ✅ Crear migraciones
- ✅ Aplicar migraciones
- ✅ Registrar modelos en admin.py
- ✅ Implementar validaciones personalizadas
- ✅ Agregar endpoints personalizados
- ✅ Documentar API
- ✅ Probar todos los métodos HTTP

---

**Autor:** Proyecto ProgII  
**Última Actualización:** 2025-01-15
