# Módulo odoo_ute - Odoo 19

## 📋 Descripción General

**odoo_ute** es un módulo completo y profesional para Odoo 19 que implementa un sistema integral de gestión universitaria. Demuestra conceptos avanzados de programación orientada a objetos, herencia, relaciones complejas en bases de datos y buenas prácticas en el desarrollo de módulos Odoo.

## 🎯 Características Principales

### 1. Modelos (Tablas) Implementados

#### **1.1 Universidad Persona (Modelo Abstracto)**
- **Clase:** `models.AbstractModel`
- **Propósito:** Base para herencia de Estudiante y Profesor
- **Campos:**
  - `name`: Nombre completo
  - `cedula`: Número único de identificación
  - `correo`: Correo electrónico
  - `telefono`: Número de contacto
  - `direccion`: Dirección física
  - `fecha_nacimiento`: Fecha de nacimiento
  - `activo`: Estado activo/inactivo
  - `edad`: Computado (calcula automáticamente)
  - `foto`: Binary (imagen de perfil)
  - `genero`: Selection (Masculino/Femenino/Otro)

- **Decoradores Implementados:**
  - `@api.depends('fecha_nacimiento')`: Calcula edad automáticamente
  - `@api.constrains('cedula', 'correo', 'fecha_nacimiento', 'edad')`: Validaciones
  - `@api.onchange('name', 'fecha_nacimiento')`: Cambios automáticos en pantalla

#### **1.2 Universidad Carrera**
- Representa programas académicos ofrecidos
- **Campos Principales:**
  - `codigo`: Identificador único
  - `nombre`: Nombre de la carrera
  - `descripcion`: Text (descripción detallada)
  - `duracion_semestres`: Integer (duración)
  - `creditos_totales`: Integer (total de créditos)
  - `estado`: Selection (Activa/Inactiva/Suspensión)
  - `porcentaje_aceptacion`: Float (% aceptación)
  - `logo`: Binary (imagen)
  - `requisitos`: Html (requisitos formateados)
  - `cantidad_estudiantes`: Computado
  - `cantidad_materias`: Computado

- **Relaciones:**
  - One2Many con Estudiante
  - Many2Many con Materia

#### **1.3 Universidad Estudiante**
- **Herencia:** Hereda de `universidad.persona`
- **Campos Específicos:**
  - `numero_matricula`: Identificador único
  - `carrera_id`: Many2One a Carrera
  - `semestre_actual`: Integer (semestre en curso)
  - `promedio_academico`: Computado (promedio de calificaciones)
  - `total_creditos_aprobados`: Computado (suma de créditos aprobados)
  - `estado_estudiante`: Selection (Activo/Inactivo/Graduado/Expulsado)
  - `fecha_ingreso`: Date (fecha de ingreso)
  - `monto_deuda`: Monetary (deuda pendiente)
  - `especialidad`: Char (concentración dentro de carrera)

- **Relaciones:**
  - Many2One con Carrera
  - One2Many con Matrícula
  - Many2Many con Materia

- **Métodos Polimórficos:**
  - `obtener_descripcion()`: Retorna "Estudiante de [Carrera] (Semestre X)"
  - `puede_graduarse()`: Verifica si puede graduarse
  - `obtener_resumen_academico()`: Resumen del desempeño

#### **1.4 Universidad Profesor**
- **Herencia:** Hereda de `universidad.persona`
- **Campos Específicos:**
  - `codigo_profesor`: Identificador único
  - `titulo_academico`: Selection (Licenciatura/Maestría/Doctorado)
  - `especialidad`: Char (área de especialización)
  - `tipo_contrato`: Selection (Tiempo Completo/Medio/Por Horas/Temporal)
  - `fecha_contratacion`: Date
  - `numero_empleado`: Char (ID de empleado)
  - `salario_base`: Monetary (salario mensual)
  - `horas_semanales`: Integer (carga horaria)
  - `calificacion_docente`: Computado (promedio de evaluaciones)
  - `anos_experiencia`: Computado (años desde contratación)
  - `estado_profesor`: Selection (Activo/Inactivo/Licencia/Retirado)
  - `certificaciones`: Html (lista de certificaciones)
  - `cv`: Binary (curriculum vitae)

- **Relaciones:**
  - One2Many con Materia

- **Métodos Polimórficos:**
  - `obtener_descripcion()`: Retorna "Profesor de [Especialidad] (PhD/Master)"
  - `puede_impartir_materia()`: Verifica si puede enseñar
  - `obtener_informacion_laboral()`: Info laboral completa

#### **1.5 Universidad Materia**
- Representa cursos ofrecidos
- **Campos Principales:**
  - `codigo`: Identificador único
  - `nombre`: Nombre del curso
  - `descripcion`: Text
  - `creditos`: Integer (créditos académicos)
  - `horas_semanales`: Integer (horas de clase)
  - `semestre`: Integer (semestre donde se ofrece)
  - `prerequisitos`: Text (requisitos previos)
  - `profesor_id`: Many2One a Profesor
  - `estado`: Selection (Activa/Inactiva)
  - `promedio_calificaciones`: Computado
  - `estudiantes_aprobados`: Computado
  - `porcentaje_aprobacion`: Computado (%)

- **Relaciones:**
  - Many2One con Profesor
  - Many2Many con Carrera
  - Many2Many con Estudiante
  - One2Many con Matrícula

#### **1.6 Universidad Matrícula**
- Registro de inscripción de estudiante en materia
- **Campos Principales:**
  - `numero_matricula`: Identificador único
  - `estudiante_id`: Many2One (Estudiante)
  - `materia_id`: Many2One (Materia)
  - `fecha_inscripcion`: Date
  - `fecha_retiro`: Date (si se retira)
  - `calificacion`: Float (0-100)
  - `tareas`: Float (calificación tareas)
  - `examenes`: Float (calificación exámenes)
  - `proyecto_final`: Float (calificación proyecto)
  - `participacion`: Float (% participación)
  - `asistencia`: Float (% asistencia)
  - `estado`: Selection (Inscrito/Cursando/Calificado/Retirado)
  - `resultado`: Computado (Aprobado/Reprobado/Pendiente)
  - `calificacion_ponderada`: Computado (promedio ponderado)
  - `creditos_ganados`: Computado (créditos si aprueba)
  - `nota_letra`: Computado (A/B/C/D/F)

- **Validaciones:**
  - Calificación entre 0-100
  - Asistencia mínima 60% para aprobar
  - Validaciones de fechas

## 🔧 Tipos de Campos Implementados

El módulo demuestra el uso de **todos** los tipos de campos disponibles en Odoo:

```python
✅ fields.Char           - Cadenas de texto (nombre, código)
✅ fields.Text           - Texto largo (descripción, observaciones)
✅ fields.Integer        - Números enteros (semestre, créditos)
✅ fields.Float          - Números decimales (promedio, porcentaje)
✅ fields.Boolean        - Verdadero/Falso (activo)
✅ fields.Date           - Fechas (fecha_nacimiento)
✅ fields.Datetime       - Fecha y hora (timestamps)
✅ fields.Selection      - Opciones predefinidas (estado, género)
✅ fields.Many2one       - Relación 1:N (estudiante -> carrera)
✅ fields.One2many       - Relación N:1 inversa (carrera -> estudiantes)
✅ fields.Many2many      - Relación N:N (estudiante -> materias)
✅ fields.Binary         - Archivos (foto, CV)
✅ fields.Html           - Contenido HTML (requisitos, certificaciones)
✅ fields.Monetary       - Moneda (salario, deuda)
```

## 🎨 Decoradores Implementados

### @api.depends
Recalcula campos computados cuando sus dependencias cambian:
- `_compute_edad()`: Recalcula edad al cambiar fecha_nacimiento
- `_compute_promedio_academico()`: Actualiza promedio al cambiar calificaciones
- `_compute_calificacion_ponderada()`: Promedio ponderado de componentes
- `_compute_nota_letra()`: Convierte número a letra

### @api.constrains
Valida datos al guardar:
- `_validar_cedula()`: Validar formato de cédula
- `_validar_correo()`: Validar formato de email
- `_validar_fecha_nacimiento()`: No puede ser futuro
- `_validar_edad_minima()`: Mínimo 18 años
- `_validar_calificacion()`: Entre 0-100
- `_validar_asistencia_minima()`: Mínimo 60%
- `_validar_duracion()`: Entre 1-16 semestres
- `_validar_creditos()`: Entre 60-500
- `_validar_semestre()`: Semestre válido

### @api.onchange
Cambios automáticos en formulario (sin guardar):
- `_onchange_name()`: Genera correo automático
- `_onchange_fecha_nacimiento()`: Recalcula edad
- `_onchange_carrera()`: Reinicia semestre a 1
- `_onchange_creditos_horas()`: Sugiere horas automáticas
- `_onchange_tipo_contrato()`: Ajusta horas según contrato
- `_onchange_calificacion()`: Actualiza estado a aprobado/reprobado

## 📊 Vistas Implementadas

### Para cada modelo se han creado **4 vistas**:

#### 1. **Vista Tree (Lista)**
- Muestra registro en formato de tabla
- Campos clave visibles de un vistazo
- Permite acciones rápidas

#### 2. **Vista Form (Formulario)**
- Formulario detallado con múltiples tabs
- Campos organizados por categorías
- Smart buttons para acciones rápidas
- Notebook con tabs para información relacionada
- Status bars para estados
- Chatter para mensajes y actividades

#### 3. **Vista Search (Búsqueda)**
- Filtros predefinidos por estado
- Búsqueda por múltiples campos
- Agrupación por categorías
- Operadores de búsqueda avanzada

#### 4. **Vista Kanban (Board)**
- Vista tipo tablero visual
- Agrupación por estado o categoría
- Tarjetas con información resumida
- Imágenes de avatar para personas

## 🔐 Seguridad y Control de Acceso

### Grupos Implementados:

1. **Usuario Universidad** (`group_usuario_universidad`)
   - Solo lectura en todos los modelos
   - Ver información sin poder modificar

2. **Administrador Universidad** (`group_admin_universidad`)
   - Crear, leer, editar y eliminar
   - Todos los permisos en todos los modelos

### Permisos por Modelo (`ir.model.access.csv`):

```csv
access_carrera_usuario         - Carrera: Usuario (R)
access_carrera_admin           - Carrera: Admin (CRUD)
access_profesor_usuario        - Profesor: Usuario (R)
access_profesor_admin          - Profesor: Admin (CRUD)
access_materia_usuario         - Materia: Usuario (R)
access_materia_admin           - Materia: Admin (CRUD)
access_estudiante_usuario      - Estudiante: Usuario (R)
access_estudiante_admin        - Estudiante: Admin (CRUD)
access_matricula_usuario       - Matrícula: Usuario (R)
access_matricula_admin         - Matrícula: Admin (CRUD)
```

### Reglas de Seguridad (`security.xml`):

- Reglas basadas en grupos
- Un usuario = Solo lectura
- Admin = Acceso completo
- Reglas extensibles y configurables

## 📋 Menús y Acciones

### Estructura de Menús:

```
📚 Universidad
├── 📖 Gestión Académica
│   ├── Carreras
│   ├── Materias
│   └── Matrículas
├── 👥 Usuarios
│   ├── Estudiantes
│   └── Profesores
└── 📊 Reportes
    └── Reportes Académicos
```

Cada modelo tiene:
- `ir.actions.act_window` para abrir vistas
- Menú principal con submenu
- Icono personalizado
- Mensajes de ayuda

## 💾 Datos Demo

El módulo incluye **20 registros de matrículas** con datos realistas:

- **10 Estudiantes** con información completa
- **5 Profesores** con especialidades variadas
- **5 Carreras** de diferentes facultades
- **10 Materias** distribuidas en semestres
- **20 Matrículas** con calificaciones variadas

Todos los datos son coherentes y se pueden usar para pruebas inmediatas.

## 🏗️ Estructura de Directorios

```
odoo_ute/
├── __init__.py                 # Inicializador del módulo
├── __manifest__.py             # Metadatos del módulo
├── models/
│   ├── __init__.py
│   ├── universidad_persona.py        # Base abstracta
│   ├── universidad_estudiante.py     # Hereda de Persona
│   ├── universidad_profesor.py       # Hereda de Persona
│   ├── universidad_carrera.py
│   ├── universidad_materia.py
│   └── universidad_matricula.py
├── views/
│   ├── universidad_carrera_views.xml
│   ├── universidad_profesor_views.xml
│   ├── universidad_materia_views.xml
│   ├── universidad_estudiante_views.xml
│   ├── universidad_matricula_views.xml
│   └── universidad_menus.xml
├── security/
│   ├── security.xml            # Grupos y reglas
│   └── ir_model_access.csv     # Permisos
├── data/
│   └── demo.xml                # Datos de demostración
├── static/
│   └── description/
│       └── icon.png            # Icono del módulo
└── README.md                   # Este archivo
```

## 🚀 Instalación y Uso

### 1. Copiar el Módulo
```bash
# Copiar la carpeta odoo_ute a:
~/odoo/custom-addons/
```

### 2. Instalar el Módulo en Odoo
```bash
# En la terminal de Odoo o mediante la interfaz:
# Aplicaciones > Actualizar Lista de Aplicaciones
# Buscar "odoo_ute"
# Hacer clic en Instalar
```

### 3. Cargar Datos Demo
Los datos demo se cargan automáticamente al instalar.

### 4. Acceder al Módulo
```
Menú Superior > Universidad
```

## 🔄 Relaciones Entre Modelos

```
                    ┌─────────────────────────────┐
                    │  Universidad.Persona        │ (Abstracto)
                    │  (Base para herencia)       │
                    └──────────┬──────────────────┘
                              /|\
                             / │ \
                            /  │  \
                           /   │   \
                ┌─────────┘    │    └──────────┐
                │              │               │
        ┌───────▼────────┐ ┌──▼──────────┐  ┌─▼────────────┐
        │   Estudiante   │ │  Profesor   │  │   (Otros)    │
        └────────┬───────┘ └──┬──────────┘  └──────────────┘
                 │            │
                 │ FK      FK │
                 │            │
         ┌───────▼────────┐   │
         │  Carrera       │   │
         │  (1 : N)       │   │
         └────────────────┘   │
                 △             │
                 │ M:N         │
         ┌───────┴────────┐    │
         │   Materia      │◄───┘
         │  (profesor)    │
         └────────┬───────┘
                  │
                  │ 1:N
                  │
         ┌────────▼───────┐
         │   Matrícula    │
         │  (inscripción) │
         └────────────────┘

Relaciones Clave:
- Carrera: 1 Carrera → N Estudiantes (One2Many)
- Materia: 1 Profesor → N Materias (One2Many)
- Matería-Carrera: M:N (Many2Many)
- Materia-Estudiante: M:N vía Matrícula
- Matrícula: N:1 relación entre Estudiante y Materia
```

## 💡 Conceptos Avanzados Implementados

### 1. **Herencia Orientada a Objetos**
```python
class UniversidadEstudiante(models.Model):
    _inherit = ['universidad.persona', 'mail.thread', ...]
    # Hereda todos los campos y métodos de Persona
```

### 2. **Polimorfismo**
```python
# Método en Persona (genérico)
def obtener_descripcion(self):
    return f"Persona: {self.name}"

# Sobrescrito en Estudiante (específico)
def obtener_descripcion(self):
    return f"Estudiante de {self.carrera_id.nombre}"

# Sobrescrito en Profesor (específico)
def obtener_descripcion(self):
    return f"Profesor de {self.especialidad}"
```

### 3. **Campos Computados con Dependencias**
```python
@api.depends('matricula_ids.calificacion')
def _compute_promedio(self):
    # Se actualiza automáticamente cuando cambian las calificaciones
```

### 4. **Validaciones Complejas**
```python
@api.constrains('asistencia')
def _validar_asistencia(self):
    # Validación que se ejecuta al guardar
```

### 5. **Cambios Automáticos en Formulario**
```python
@api.onchange('creditos')
def _onchange_creditos(self):
    # Se ejecuta mientras se edita, sin guardar
    self.horas_semanales = self.creditos
```

### 6. **Chat y Actividades**
```python
_inherit = ['mail.thread', 'mail.activity.mixin']
# Añade automáticamente chatter y seguimiento
```

## 📈 Campos Computados

### Automáticos:
- **edad**: Calcula años desde fecha_nacimiento
- **cantidad_estudiantes**: Cuenta estudiantes de una carrera
- **promedio_academico**: Promedio de calificaciones
- **resultado**: Aprobado/Reprobado basado en calificación
- **creditos_ganados**: Solo si aprueba la materia
- **nota_letra**: Convierte número a A,B,C,D,F
- **calificacion_ponderada**: Promedio ponderado
- **calificacion_docente**: Promedio de evaluaciones del profesor
- **anos_experiencia**: Años desde contratación
- **porcentaje_aprobacion**: % de estudiantes aprobados

## 🎓 Casos de Uso

### 1. Gestión de Carrera Completa
- Crear carrera
- Asignar materias
- Ver estudiantes inscritos
- Monitorear desempeño

### 2. Gestión de Profesor
- Crear perfil de profesor
- Asignar materias
- Ver calificación docente
- Gestionar información laboral

### 3. Inscripción de Estudiante
- Crear estudiante
- Inscribir en carrera
- Registrar matrículas
- Seguimiento de calificaciones

### 4. Evaluación de Desempeño
- Registrar calificaciones
- Calcular promedios automáticos
- Determinar si aprueba
- Generar reportes

## 🛠️ Funcionalidades Extras

- ✅ Mail threading (comentarios)
- ✅ Activity management (tareas)
- ✅ Status bars (seguimiento de estado)
- ✅ Smart buttons (acceso rápido)
- ✅ Progreso visual (progress bars)
- ✅ Kanban customizado
- ✅ Búsqueda avanzada
- ✅ Filtros predefinidos
- ✅ Agrupación flexible
- ✅ Widgets especializados

## 📝 Notas Importantes

1. **Herencia Abstracta**: El modelo `universidad.persona` es abstracto (`models.AbstractModel`), por lo que no crea tabla propia. Sus campos se heredan en Estudiante y Profesor.

2. **Mail Mixins**: Los modelos incluyen `mail.thread` y `mail.activity.mixin` para habilitar comentarios y actividades.

3. **Seguridad por Defecto**: Usuarios normales solo leen, administradores tienen acceso completo.

4. **Datos Realistas**: Los datos demo incluyen nombres ecuatorianos realistas y datos coherentes.

5. **Validaciones**: Todas las validaciones se ejecutan al guardar, los cambios en pantalla con @api.onchange no requieren guardado.

## 👨‍💼 Autor

**Módulo Universidad UTE**
- Institución: Universidad Técnica Estatal (UTE)
- Curso: Programación II
- Versión: 17.0.1.0.0
- Licencia: LGPL-3

---

**Proyecto completo listo para usar en Odoo 17** ✨
