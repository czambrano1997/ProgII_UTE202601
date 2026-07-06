# Django REST API - Proyecto Completo

API REST completa con 5 modelos (Category, Product, Customer, Order, Review) usando Django 6.0 y Django REST Framework.

## 🚀 Quick Start

### Instalación y Setup
```bash
cd c:\Users\jandry\OneDrive\Desktop\djangoapi
.venv\Scripts\python.exe manage.py migrate
.venv\Scripts\python.exe manage.py runserver
```

Servidor disponible en: **http://127.0.0.1:8000/**

### Endpoints API
- **Categories:** `GET/POST /api/categories/`
- **Products:** `GET/POST /api/products/`
- **Customers:** `GET/POST /api/customers/`
- **Orders:** `GET/POST /api/orders/`
- **Reviews:** `GET/POST /api/reviews/`

Cada endpoint soporta: `GET`, `POST`, `PUT`, `PATCH`, `DELETE`

## 📊 Estructura

```
djangov2/
├── models.py          # 5 modelos de la base de datos
├── serializers.py     # Serializers con validaciones
├── views.py           # ViewSets para CRUD
├── urls.py            # Rutas de la API
├── tests.py           # 60+ tests automatizados
├── admin.py           # Administrador Django
└── migrations/        # Migraciones de BD
```

## ✅ Características

✓ **5 Modelos CRUD** - Category, Product, Customer, Order, Review  
✓ **Validaciones** - En todos los campos con mensajes claros  
✓ **60+ Tests** - Cobertura completa de endpoints  
✓ **Documentación** - Ver `DOCUMENTACION.md` para detalles completos  
✓ **Admin Django** - Registrado y configurado  

## 🧪 Ejecutar Tests
```bash
.venv\Scripts\python.exe manage.py test djangov2 -v 2
```

## 📚 Documentación Completa
Ver **`DOCUMENTACION.md`** para:
- Descripción completa de modelos
- Ejemplos de todas las operaciones CRUD
- Validaciones y restricciones
- Códigos de error
- Ejemplos con cURL

---

**Última actualización:** 5 de Julio, 2026
