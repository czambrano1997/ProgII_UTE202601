# 🧑‍💻 Programación II – 2026-01  
## Repositorio de Módulos Odoo 19

Este repositorio contiene los módulos desarrollados por los estudiantes de la asignatura **Programación II** durante el periodo **2026-01**. Cada estudiante trabaja en su propia rama, donde se alojan los módulos personalizados para Odoo 19 dentro de la carpeta `odoo/custom-addons`.

---

## 📁 Estructura del repositorio
.
├── README.md # Este archivo
└── (Ramas por estudiante)
└── [nombre_estudiante]
└── custom-addons/ # Directorio donde se almacenan los módulos desarrollados
├── scripts/ # Directorio donde se almacenan scripts utilizados
└── ...


- **Rama principal (`main` / `master`)**: contiene únicamente este `README.md` y sirve como punto de partida.
- **Ramas por estudiante**: cada estudiante tiene su propia rama con el nombre `apellido_nombre` (ej. `perez_juan`). En ella encontrará el directorio `custom-addons/` listo para agregar sus módulos.

---

## 🚀 Cómo empezar a trabajar

### 1. Clonar el repositorio
```bash
git clone <url-del-repositorio>
cd <nombre-del-repositorio>
```

### 2. Cambiar a tu rama personal
Si tu rama ya existe:
```bash
git checkout apellido_nombre
```

Si aún no existe, créala a partir de la rama **main:**
```bash
git checkout -b apellido_nombre main
git push -u origin apellido_nombre
```


