# Cancha Manager - Sistema de Gestión de Canchas

Sistema completo de gestión de canchas de futbol con Django, desarrollado para manejar clientes, reservas, paquetes, inventario y consumo de productos.

## 📋 Módulos Principales

### 1. **Clientes** (`/djangov1/cliente/`)
- Gestiona la base de datos de clientes
- Almacena: nombre, apellido, email, teléfono
- Registra fecha de registro automática
- Permite editar y eliminar clientes

### 2. **Reservas** (`/djangov1/reserva/`)
- Crea y administra reservas de canchas
- Asocia clientes con reservas
- Registra horarios (llegada/salida)
- Asigna paquetes y calcula pagos
- Controla cantidad de jugadores

### 3. **Paquetes** (`/djangov1/paquete/`)
- Define servicios personalizados
- Establece costos por paquete
- Incluye descripciones detalladas
- Se asocian a las reservas

### 4. **Inventario** (`/djangov1/inventario/`)
- Control de productos disponibles
- Precio unitario y cantidad en stock
- Alertas para productos con stock bajo (≤5)
- Registro de fecha de entrada

### 5. **Gestión de Reservas** (`/djangov1/gestion_reserva/`)
- Verifica si los clientes llegaron
- Asocia productos consumidos a reservas
- Controla detalles de cada reserva realizada

### 6. **Consumo** (`/djangov1/consumo/`)
- Registra productos consumidos por cliente
- Calcula costos de consumo
- Vincula consumo con gestión de reservas

## 🗄️ Modelos de Datos

### Cliente
```python
- nombre (CharField, max 100)
- segundo_nombre (CharField, max 100, opcional)
- apellido (CharField, max 100)
- segundo_apellido (CharField, max 100, opcional)
- email (EmailField, único)
- teléfono (CharField, max 15)
- fecha_registro (DateField, auto)
```

### Reserva
```python
- cliente (ForeignKey → Cliente)
- número_reserva (AutoField, primary key)
- hora_llegada (TimeField)
- hora_salida (TimeField)
- pago (DecimalField)
- cantidad_jugadores (IntegerField)
- paquete (ForeignKey → Paquete, opcional)
- nota (TextField)
```

### Paquete
```python
- nombre_paquete (CharField, max 100)
- costo_paquete (DecimalField)
- descripción (TextField)
```

### Inventario
```python
- nombre_producto (CharField, max 100, opcional)
- precio_unitario (DecimalField, opcional)
- cantidad_producto (IntegerField, opcional)
- fecha_registro (DateTimeField, auto)
```

### Gestión de Reserva
```python
- cliente (OneToOneField → Cliente)
- reserva (ForeignKey → Reserva)
- llegó (BooleanField, default=False)
- productos_consumidos (ManyToManyField → Inventario, through DetalleConsumo)
```

### Detalle de Consumo
```python
- gestión (ForeignKey → Gestión_reserva)
- producto (ForeignKey → Inventario)
- cantidad (PositiveIntegerField)
```

## 🚀 Instalación y Configuración

### Requisitos
- Python 3.8+
- Django 6.0+
- PostgreSQL (configurado en settings.py)

### Pasos

1. **Instalar dependencias:**
```bash
pip install django psycopg2-binary
```

2. **Configurar base de datos:**
Editar `core/settings.py` con credenciales de PostgreSQL

3. **Ejecutar migraciones:**
```bash
python manage.py migrate
```

4. **Crear superusuario:**
```bash
python manage.py createsuperuser
```

5. **Recopilar archivos estáticos:**
```bash
python manage.py collectstatic
```

6. **Ejecutar servidor:**
```bash
python manage.py runserver
```

## 📍 URLs Disponibles

| Página | URL | Nombre |
|--------|-----|--------|
| Inicio | `/djangov1/` | home_futbol |
| Clientes | `/djangov1/cliente/` | clientes_futbol |
| Reservas | `/djangov1/reserva/` | hacer_reservas |
| Paquetes | `/djangov1/paquete/` | paquetes_futbol |
| Inventario | `/djangov1/inventario/` | inventario_canchas |
| Gestión | `/djangov1/gestion_reserva/` | gestionar_reservas |
| Consumo | `/djangov1/consumo/` | consumo_cliente |
| Admin | `/admin/` | - |

## 🎨 Diseño y Estilos

- **Color Primario:** #2f6b4f (Verde oscuro)
- **Fondo:** #f7f6f2 (Beige claro)
- **Tipografía:** Sistema FontStack estándar
- **Responsive:** Adaptado para dispositivos móviles

### Archivos CSS
- `djangov1/static/djangov1/estilo.css` - Estilos principales

## 📝 Uso de Plantillas

Todas las plantillas usan:
- Template tags de Django (`{% load static %}`, `{% url %}`)
- Bucles para iterar datos (`{% for %}...{% endfor %}`)
- Condicionales (`{% if %}...{% endif %}`)
- Filtros (`{{ variable|date:"d/m/Y" }}`)

## 🔧 Características Administrativas

Acceso a través de `/admin/`:
- Crear, editar, eliminar clientes
- Gestionar reservas y paquetes
- Administrar inventario
- Registrar consumo de productos
- Control completo de datos

## 📊 Estadísticas

La página de inicio muestra:
- Total de clientes registrados
- Total de reservas realizadas
- Paquetes disponibles
- Productos en stock

## 🛠️ Archivos Creados/Modificados

### Templates
- ✅ `clientes.html` - Lista de clientes
- ✅ `reservas.html` - Lista de reservas
- ✅ `paquete.html` - Lista de paquetes
- ✅ `inventario.html` - Gestión de inventario
- ✅ `gestion_reservas.html` - Gestión de reservas
- ✅ `consumo.html` - Registro de consumo
- ✅ `home.html` - Página de inicio

### CSS
- ✅ `djangov1/static/djangov1/estilo.css` - Estilos completos

### Python
- ✅ `views.py` - Vistas actualizadas con Home
- ✅ `urls.py` - URLs configuradas
- ✅ `settings.py` - Configuración de estáticos

## 📌 Notas Importantes

1. **Base de datos:** Requiere PostgreSQL configurado y ejecutándose
2. **Estáticos en desarrollo:** Django sirve los estáticos automáticamente en DEBUG=True
3. **Producción:** Ejecutar `collectstatic` antes de desplegar
4. **Admin:** Todos los modelos están registrados y listos para usar

## 🐛 Posibles Mejoras Futuras

- [ ] Formularios para crear/editar registros desde la web
- [ ] API REST con Django REST Framework
- [ ] Reportes de ingresos y consumo
- [ ] Autenticación de usuarios por cliente
- [ ] Integración con pasarelas de pago
- [ ] Notificaciones por email
- [ ] Gráficas de estadísticas
- [ ] Búsqueda y filtros avanzados

---

**Desarrollado con Django 6.0 | PostgreSQL | HTML5/CSS3**