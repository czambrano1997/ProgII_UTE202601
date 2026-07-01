# Guía paso a paso — Pruebas en Odoo (`odoo_ute`)

Este documento explica qué se hizo en el módulo `odoo_ute` y cómo correr sus
pruebas tú mismo. Sigue el patrón `TransactionCase` visto en clase (pruebas
funcionales + de seguridad sobre modelos de negocio, en una transacción que
se revierte automáticamente al terminar cada test).

---

## 1. Qué se corrigió y qué se agregó

### Bug bloqueante corregido

El módulo **no instalaba en limpio**. En algún momento se renombró el modelo
en `models/teacher.py`:

```python
_name = 'ou.teacher'   # antes
_name = 'sistema.usuarios'   # ahora
```

...pero `views/teacher.xml`, `security/ir.model.access.csv` y
`security/ute_rule.xml` seguían apuntando al nombre técnico viejo
(`ou.teacher` / `model_ou_teacher`), que ya no existe. Se corrigieron las
tres referencias para que apunten a `sistema.usuarios` / `model_sistema_usuarios`.
Se verificó instalando el módulo desde cero en una base de datos descartable.

> En tu base de trabajo (`testUTE`) esto no se notaba porque el módulo quedó
> instalado desde *antes* del rename — pero cualquiera que lo instale de cero
> (un compañero, el profesor, o tú en otra máquina) se topaba con el error
> `No matching record found for external id 'model_ou_teacher'`.

### Pruebas agregadas

```
odoo_ute/
└── tests/
    ├── __init__.py
    ├── test_teacher.py     # unitarias/funcionales sobre sistema.usuarios
    ├── test_signature.py    # unitarias sobre ou.signature
    └── test_security.py      # seguridad: accesos por grupo
```

Y se agregó `from . import tests` en `odoo_ute/__init__.py` (así Odoo carga
las clases de test cuando el módulo se instala/actualiza con `--test-enable`).

---

## 2. Preparar el entorno

Ya tienes todo instalado (Odoo 19 + Postgres 16 + el entorno virtual con las
dependencias de Odoo). Solo confirma que Postgres esté levantado:

```bash
psql -h 127.0.0.1 -U odoo -d testUTE -c "\dt" | head
```

Las credenciales están en `odoo.conf` (raíz del repo):

```ini
db_host = 127.0.0.1
db_port = 5432
db_user = odoo
db_password = odoo
addons_path = .../odoo-19.0/addons,.../odoo-19.0/odoo/addons,.../odoo/custom-addons,
```

---

## 3. Ejecutar las pruebas

**Importante**: no corras `--test-enable` directamente sobre `testUTE` para
un `-i` (instalación desde cero) — usa una base descartable para no perder
tus datos de prueba. Si solo vas a **actualizar** el módulo en `testUTE` (con
`-u`, no `-i`), sí es seguro, porque `-u` no recrea la base.

### Opción A — Base descartable (recomendado para solo correr las pruebas)

```bash
cd ProgII_UTE202601

# Crear una base nueva y vacía
createdb -h 127.0.0.1 -U odoo mi_bd_pruebas

# Instalar el módulo + correr sus pruebas
python odoo-19.0/odoo-bin \
  -c odoo.conf \
  -d mi_bd_pruebas \
  -i odoo_ute \
  --test-enable \
  --test-tags /odoo_ute \
  --stop-after-init

# (opcional) borrar la base al terminar
dropdb -h 127.0.0.1 -U odoo mi_bd_pruebas
```

### Opción B — Sobre tu base de trabajo (`testUTE`), actualizando el módulo

```bash
python odoo-19.0/odoo-bin \
  -c odoo.conf \
  -d testUTE \
  -u odoo_ute \
  --test-enable \
  --test-tags /odoo_ute \
  --stop-after-init
```

### Filtrar solo un archivo de pruebas

```bash
--test-tags /odoo_ute:TestSeguridad     # solo test_security.py
--test-tags /odoo_ute:TestTeacher       # solo test_teacher.py
```

---

## 4. Qué prueba cada archivo

| Archivo | Qué valida |
|---|---|
| `tests/test_teacher.py` | Creación del docente (`sistema.usuarios`); el campo computado `validate_email` (`'Validado'` si el email tiene `@`, `'No valido'` si no o si está vacío); la validación `_check_vat` (CI/RUC con menos de 10 caracteres lanza `ValidationError`); las relaciones M2M (`signature_ids`) y M2O (`signature_primary`) hacia `ou.signature`. |
| `tests/test_signature.py` | Creación de materias (`ou.signature`) y que registros distintos tengan ids distintos. |
| `tests/test_security.py` | **Seguridad** (como el ejemplo de la diapositiva 7): un usuario del grupo `Usuario` (`perm_create=0` en `ir.model.access.csv`) recibe `AccessError` al intentar crear un docente; un usuario del grupo `Administrador` (`perm_create=1`) sí puede. |

---

## 5. Cómo leer la salida

Al final del log vas a ver una línea como esta:

```
... odoo.tests.result: 0 failed, 0 error(s) of 12 tests when loading database '...'
```

- `0 failed` → ninguna aserción (`assertEqual`, `assertRaises`, etc.) falló.
- `0 error(s)` → ningún test lanzó una excepción inesperada (por ejemplo, un
  error de configuración como el `groups_id` → `group_ids` que se corrigió
  al escribir `test_security.py`, cuando Odoo 19 renombró ese campo).
- Si algo sale mal, busca hacia arriba en el log la línea
  `ERROR: TestClase.test_metodo` — ahí está el traceback completo.

---

## 6. Errores comunes

- **`No matching record found for external id 'model_ou_teacher'`** → ya
  corregido (ver sección 1). Si vuelve a aparecer, es que algún archivo nuevo
  quedó referenciando el nombre técnico viejo del modelo.
- **`Invalid field 'groups_id' in 'res.users'`** → en Odoo 19 el campo se
  llama `group_ids` (no `groups_id`, como en versiones anteriores de Odoo).
- **`FATAL: password authentication failed`** → revisa `db_user`/`db_password`
  en `odoo.conf` contra tu Postgres local.
- **Las pruebas no corren / "0 tests"** → falta `--test-enable` y
  `--test-tags /odoo_ute` en el comando, o el módulo no se está
  instalando/actualizando (`-i`/`-u`) en ese mismo comando.

---

## 7. Resultado esperado

```
odoo.tests.result: 0 failed, 0 error(s) of 12 tests when loading database '...'
```

(Verificado localmente instalando el módulo desde cero en una base descartable
— no se tocó `testUTE`.)
