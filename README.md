# 🧑‍💻 Programación II – UTE (Periodo 2026-01)
## Repositorio de la materia Programación II

Este repositorio es el espacio de trabajo central para los estudiantes de la asignatura **Programación II**. Aquí se gestionarán los módulos personalizados desarrollados tanto para **Odoo 19** como para **Django**, permitiendo un seguimiento individualizado de cada proyecto.

---

## 📂 Organización del Repositorio

El flujo de trabajo se basa en una estructura de ramas independiente para cada estudiante:

- **Rama `main`**: Contiene la documentación general y plantillas base. No se debe trabajar directamente en esta rama.
- **Ramas de Estudiantes**: Cada alumno contará con su propia rama siguiendo el formato:
  `estudiante/apellido_nombre`  *(Ejemplo: `estudiante/zambrano_ceider`)*
- **Directorio de Módulos**: Dentro de cada rama, el código debe residir en:
  `odoo/custom-addons/` o `django/custom-addons/`

---

## 🛠️ Guía de Trabajo para el Estudiante

### 1. Preparación del Entorno
Clona el repositorio en tu máquina local:
```bash
git clone <URL_DEL_REPOSITORIO>
cd <NOMBRE_DEL_REPOSITORIO>
```

### 2. Creación de tu Espacio de Trabajo
Si aún no tienes tu rama, créala desde `main`:
```bash
git checkout -b estudiante/tu-apellido-tu-nombre
git push -u origin estudiante/tu-apellido-tu-nombre
```

### 3. Desarrollo de Módulos
Todos tus módulos de Odoo deben estar dentro de la carpeta `odoo/custom-addons` o `django/custom-addons` según corresponda.
```text
README.md # Este archivo
scripts
└── scriptOdoo19.sh
odoo/custom-addons
└── modulo_estudiante
    ├── __init__.py
    ├── __manifest__.py
    ├── models/
    ├── views/
    └── security/
django/custom-addons
└── modulo_estudiante
    ├── __init__.py
    ├── __manifest__.py
    ├── models/
    ├── views/
    └── security/
```

### 4. Ejemplo, cómo agregar módulos
**En Odoo**
Añade tus módulos dentro de odoo/custom-addons/ y añadelo a tu addons_path. Por ejemplo:
```ini
addons_path = ..,/ruta/al/repositorio/odoo-custom-addons
```

### 5. Subir cambios al repositorio
Una vez realizado los cambios necesarios, deberás añadirlos al repositorio:
```ini
git add odoo/custom-addons/mimodulo/
git commit -m"Se añade un nuevo módulo para la creación de estudiantes (...)"
git push origin apellido_nombre
```

---

## 📝 Convenciones y Buenas Prácticas

- **Commits**: Usa mensajes descriptivos en español (Ej: `feat: agrega modelo de préstamos`).
- **Nombres de módulos**: Usa snake_case y prefijos si es necesario (Ej: `ute_gestion_biblioteca`).
- **Seguridad**: Asegúrate de incluir siempre los archivos de acceso (`ir.model.access.csv`) para tus nuevos modelos.

---

## ⚙️ Configuración del entorno de desarrollo para Odoo
Para probar los módulos localmente, necesitarás tener instalado Odoo 19 con Python 3.12 y PostgreSQL v16.
Se recomienda usar el script de instalación automática proporcionado por la cátedra (disponible en el material del curso), que configura:

-- Entorno virtual Python (.venv)
-- Base de datos PostgreSQL con usuario y permisos adecuados
-- Archivo odoo.conf con el addons_path que incluye custom-addons

**Stack Tecnológico para Odoo**
- **Core de Odoo**: [Odoo 19](https://github.com/odoo/odoo/tree/19.0)
- **Lenguaje**: Python 3.12+
- **Base de Datos**: PostgreSQL 16+
- **Control de Versiones**: Git & GitHub

---

## 📚 Recursos útiles

- [Documentación oficial de Odoo 19](https://www.odoo.com/documentation/19.0/)
- [Guía de desarrollo de módulos Odoo](https://www.odoo.com/documentation/19.0/developer/howtos/backend.html)
- [Curso rápido de Git](https://rogerdudler.github.io/git-guide/index.es.html)


---
