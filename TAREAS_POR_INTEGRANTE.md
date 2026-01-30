# 📋 Distribución de Tareas - Grupo 5

## 🎯 Resumen del Proyecto

**Gestor de Base de Datos de Vulnerabilidades** - Mini SOC Knowledge Base con operaciones CRUD sobre vulnerabilidades tipo CVE.

---

## 👤 INTEGRANTE 1 - Backend & Base de Datos ✅ COMPLETADO

### Responsabilidad
Capa de datos y conexión con MongoDB.

### Archivos a Implementar
- ✅ `database/__init__.py`
- ✅ `database/connection.py` - Conexión a MongoDB
- ✅ `database/models.py` - Modelo de vulnerabilidades con validaciones
- ✅ `requirements.txt` - Dependencias del proyecto
- ✅ `.gitignore` - Archivos a ignorar en Git
- ✅ `.env.example` - Plantilla de configuración

### Tareas Específicas
1. ✅ Configurar conexión a MongoDB (local o Atlas)
2. ✅ Implementar modelo de datos con validaciones
3. ✅ Crear índices para optimizar búsquedas
4. ✅ Manejar errores de conexión
5. ✅ Documentar configuración en BACKEND_SETUP.md

### Entregables
- ✅ Base de datos conectada y funcionando
- ✅ Modelo de datos validado
- ✅ Documentación técnica completa

### Recursos
- Leer: `BACKEND_SETUP.md`
- Tutorial MongoDB: https://www.mongodb.com/docs/manual/
- PyMongo Docs: https://pymongo.readthedocs.io/

---

## 👤 INTEGRANTE 2 - Operaciones CRUD

### Responsabilidad
Implementar todas las operaciones de base de datos (Create, Read, Update, Delete).

### Archivos a Implementar
- [ ] `crud/__init__.py` - Exportar funciones CRUD
- [ ] `crud/create.py` - Crear nuevas vulnerabilidades
- [ ] `crud/read.py` - Leer/consultar vulnerabilidades
- [ ] `crud/update.py` - Actualizar vulnerabilidades existentes
- [ ] `crud/delete.py` - Eliminar vulnerabilidades

### Tareas Específicas

#### `crud/create.py`
```python
def create_vulnerability(db, vuln_data):
    """
    Crea una nueva vulnerabilidad en la base de datos.

    - Validar datos con VulnerabilityModel
    - Verificar que CVE_ID no exista (único)
    - Insertar en colección 'vulnerabilities'
    - Retornar ID insertado o error
    """
    pass
```

#### `crud/read.py`
```python
def get_vulnerability_by_id(db, cve_id):
    """Obtener vulnerabilidad por CVE_ID"""
    pass

def list_all_vulnerabilities(db, limit=50):
    """Listar todas las vulnerabilidades con paginación"""
    pass

def find_by_severity(db, severity):
    """Buscar por nivel de severidad"""
    pass

def find_by_status(db, status):
    """Buscar por estado (Open/Patched/Investigating)"""
    pass

def search_by_keyword(db, keyword):
    """Búsqueda de texto en título y descripción"""
    pass
```

#### `crud/update.py`
```python
def update_vulnerability(db, cve_id, update_data):
    """
    Actualizar vulnerabilidad existente.

    - Verificar que existe
    - Validar nuevos datos
    - Actualizar last_modified
    - Aplicar cambios
    """
    pass

def update_status(db, cve_id, new_status):
    """Cambiar estado de vulnerabilidad"""
    pass

def add_reference(db, cve_id, reference_url):
    """Agregar URL de referencia"""
    pass
```

#### `crud/delete.py`
```python
def delete_vulnerability(db, cve_id):
    """
    Eliminar vulnerabilidad por CVE_ID.

    - Verificar que existe
    - Confirmar eliminación
    - Borrar de BD
    """
    pass

def delete_by_status(db, status):
    """Eliminar todas las vulnerabilidades con cierto estado"""
    pass
```

### Entregables
- [ ] Funciones CRUD implementadas y funcionando
- [ ] Manejo de errores (duplicados, no encontrados, etc.)
- [ ] Validación de datos antes de operaciones
- [ ] Comentarios en código explicando lógica

### Recursos
- Usar: `from database.connection import get_database`
- Usar: `from database.models import VulnerabilityModel`
- PyMongo CRUD: https://pymongo.readthedocs.io/en/stable/tutorial.html

### Coordinación
- **Depende de**: Integrante 1 (Backend listo)
- **Coordinar con**: Integrante 3 (UI usará estas funciones)

---

## 👤 INTEGRANTE 3 - Interfaz & Utilidades

### Responsabilidad
Interfaz de usuario por consola y herramientas auxiliares.

### Archivos a Implementar
- [ ] `ui/__init__.py`
- [ ] `ui/menu.py` - Menú interactivo
- [ ] `utils/__init__.py`
- [ ] `utils/validators.py` - Validadores de entrada
- [ ] `utils/generators.py` - Generador de CVE IDs
- [ ] `utils/reports.py` - Generación de reportes
- [ ] `main.py` - Punto de entrada de la aplicación

### Tareas Específicas

#### `utils/generators.py`
```python
def generate_cve_id(db):
    """
    Generar ID único tipo CVE-2025-XXXXX.

    - Consultar último ID usado
    - Incrementar número
    - Formato: CVE-YYYY-NNNNN (5 dígitos)
    """
    pass

def generate_random_cve_id():
    """Generar ID aleatorio para testing"""
    pass
```

#### `utils/validators.py`
```python
def validate_cve_format(cve_id):
    """Validar formato CVE-YYYY-NNNNN"""
    pass

def validate_cvss_score(score):
    """Validar que score esté entre 0.0 y 10.0"""
    pass

def validate_url(url):
    """Validar formato de URL para referencias"""
    pass

def get_user_input_secure(prompt, input_type='text'):
    """Obtener entrada del usuario con validación"""
    pass
```

#### `utils/reports.py`
```python
def generate_summary_report(db):
    """
    Generar reporte de resumen:
    - Total de vulnerabilidades
    - Por severidad
    - Por estado
    - Últimas 10 registradas
    """
    pass

def export_to_json(db, filename):
    """Exportar vulnerabilidades a JSON"""
    pass

def export_to_csv(db, filename):
    """Exportar vulnerabilidades a CSV"""
    pass

def display_statistics(db):
    """Mostrar estadísticas en consola"""
    pass
```

#### `ui/menu.py`
```python
def show_main_menu():
    """
    Mostrar menú principal:

    === GESTOR DE VULNERABILIDADES ===
    1. Registrar nueva vulnerabilidad
    2. Consultar vulnerabilidad
    3. Listar todas las vulnerabilidades
    4. Buscar por severidad
    5. Actualizar vulnerabilidad
    6. Eliminar vulnerabilidad
    7. Generar reporte
    8. Salir
    """
    pass

def menu_create_vulnerability(db):
    """Flujo para crear vulnerabilidad"""
    pass

def menu_search_vulnerability(db):
    """Flujo para buscar vulnerabilidades"""
    pass

def menu_update_vulnerability(db):
    """Flujo para actualizar"""
    pass

def menu_delete_vulnerability(db):
    """Flujo para eliminar"""
    pass

def menu_generate_report(db):
    """Flujo para reportes"""
    pass

def main_loop():
    """Loop principal de la aplicación"""
    pass
```

#### `main.py`
```python
"""
Punto de entrada de la aplicación.

1. Conectar a base de datos
2. Mostrar mensaje de bienvenida
3. Iniciar loop de menú
4. Cerrar conexión al salir
"""

from database.connection import get_database, close_connection
from ui.menu import main_loop

if __name__ == "__main__":
    try:
        print("🔐 Gestor de Vulnerabilidades - Iniciando...")
        db = get_database()
        main_loop()
    except KeyboardInterrupt:
        print("\n\n👋 Saliendo...")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        close_connection()
        print("✅ Aplicación cerrada")
```

### Entregables
- [ ] Interfaz de consola interactiva
- [ ] Generador de CVE IDs automático
- [ ] Sistema de reportes funcionando
- [ ] Exportación a JSON/CSV
- [ ] `main.py` ejecutable

### Recursos
- Colorama (colores en consola): https://pypi.org/project/colorama/
- Tabulate (tablas): https://pypi.org/project/tabulate/

### Coordinación
- **Depende de**: Integrante 1 (Backend) e Integrante 2 (CRUD)
- **Coordinar con**: Todos (usa funciones de todos los módulos)

---

## 👤 INTEGRANTE 4 - Testing & Documentación

### Responsabilidad
Pruebas, datos de ejemplo y documentación del proyecto.

### Archivos a Implementar
- [ ] `tests/__init__.py`
- [ ] `tests/sample_data.py` - Datos de ejemplo
- [ ] `tests/test_database.py` - Tests de conexión
- [ ] `tests/test_crud.py` - Tests de operaciones CRUD
- [ ] `tests/test_models.py` - Tests de validación
- [ ] `USER_GUIDE.md` - Guía de usuario
- [ ] `API_DOCS.md` - Documentación de funciones

### Tareas Específicas

#### `tests/sample_data.py`
```python
"""
Crear datos de ejemplo realistas:
- 10-15 vulnerabilidades variadas
- Diferentes severidades (Critical, High, Medium, Low)
- Diferentes estados (Open, Patched, Investigating)
- Sistemas reales (Apache, Nginx, MySQL, etc.)
"""

def get_sample_vulnerabilities():
    """Retornar lista de vulnerabilidades de ejemplo"""
    return [
        {
            'cve_id': 'CVE-2025-00001',
            'title': 'SQL Injection en MySQL 8.0',
            'description': 'Vulnerabilidad de inyección SQL...',
            'severity': 'Critical',
            'cvss_score': 9.8,
            'affected_systems': ['MySQL 8.0.x'],
            'status': 'Open',
            'references': ['https://...'],
            'mitigation': 'Actualizar a 8.0.35'
        },
        # ... más vulnerabilidades
    ]

def populate_database_with_samples(db):
    """Poblar BD con datos de ejemplo"""
    pass

def clear_test_data(db):
    """Limpiar datos de prueba"""
    pass
```

#### `tests/test_database.py`
```python
"""Tests de conexión a base de datos"""

def test_connection():
    """Probar conexión a MongoDB"""
    pass

def test_database_creation():
    """Verificar que la BD se crea correctamente"""
    pass

def test_indexes():
    """Verificar que los índices existen"""
    pass
```

#### `tests/test_crud.py`
```python
"""Tests de operaciones CRUD"""

def test_create_vulnerability():
    """Probar creación de vulnerabilidad"""
    pass

def test_read_vulnerability():
    """Probar lectura"""
    pass

def test_update_vulnerability():
    """Probar actualización"""
    pass

def test_delete_vulnerability():
    """Probar eliminación"""
    pass

def test_duplicate_cve_id():
    """Verificar que no se permiten duplicados"""
    pass
```

#### `tests/test_models.py`
```python
"""Tests de validación de modelo"""

def test_valid_vulnerability():
    """Probar datos válidos"""
    pass

def test_invalid_severity():
    """Probar severidad inválida"""
    pass

def test_invalid_cvss():
    """Probar CVSS fuera de rango"""
    pass

def test_missing_required_fields():
    """Probar campos obligatorios faltantes"""
    pass
```

#### `USER_GUIDE.md`
```markdown
# Guía de Usuario - Gestor de Vulnerabilidades

## Instalación
[Paso a paso para instalar]

## Uso Básico
[Screenshots y ejemplos de cada función]

## Casos de Uso
1. Registrar nueva vulnerabilidad
2. Buscar vulnerabilidades críticas
3. Actualizar estado a "Patched"
4. Generar reporte mensual

## Preguntas Frecuentes (FAQ)
```

#### `API_DOCS.md`
```markdown
# Documentación de API

## Módulo database

### connection.py
- `get_database()`: Descripción, parámetros, retorno
- `close_connection()`: ...

### models.py
- `VulnerabilityModel`: ...

## Módulo crud
[Documentar todas las funciones]

## Módulo utils
[Documentar todas las funciones]
```

### Tareas de Testing
1. [ ] Ejecutar todas las pruebas y verificar que pasen
2. [ ] Probar el flujo completo de la aplicación
3. [ ] Documentar bugs encontrados
4. [ ] Verificar que todas las funciones tengan comentarios
5. [ ] Crear video/screenshots de demo

### Entregables
- [ ] 10-15 vulnerabilidades de ejemplo insertadas
- [ ] Tests unitarios implementados
- [ ] Guía de usuario completa con ejemplos
- [ ] Documentación de API
- [ ] Reporte de testing (qué funciona, qué falta)

### Recursos
- Pytest (testing): https://docs.pytest.org/
- Unittest (incluido en Python): https://docs.python.org/3/library/unittest.html

### Coordinación
- **Depende de**: Todos los integrantes
- **Rol**: Verificar que todo funciona correctamente

---

## 📅 Cronograma Sugerido

### Semana 1
- **Integrante 1**: Setup de backend (✅ COMPLETADO)
- **Integrante 2**: Iniciar CRUD (create y read)
- **Integrante 3**: Diseñar menú y generadores
- **Integrante 4**: Crear datos de ejemplo

### Semana 2
- **Integrante 2**: Completar CRUD (update y delete)
- **Integrante 3**: Implementar UI completa
- **Integrante 4**: Tests unitarios

### Semana 3
- **Todos**: Integración y pruebas
- **Integrante 4**: Documentación final
- **Todos**: Preparar presentación

---

## 🔄 Flujo de Trabajo Git

### Para cada integrante:

1. **Actualizar repo**
```bash
git pull origin main
```

2. **Crear tu rama**
```bash
git checkout -b feature/tu-nombre-modulo
```

3. **Trabajar en tu código**
```bash
# Hacer cambios...
git add .
git commit -m "Descripción clara de cambios"
```

4. **Subir cambios**
```bash
git push origin feature/tu-nombre-modulo
```

5. **Crear Pull Request en GitHub**
- Ir al repositorio
- Botón "New Pull Request"
- Descripción de cambios
- Solicitar revisión de equipo

---

## ✅ Checklist General del Proyecto

### Funcionalidad
- [ ] Conexión a MongoDB funcionando
- [ ] CRUD completo implementado
- [ ] Interfaz de usuario interactiva
- [ ] Generación de CVE IDs automática
- [ ] Sistema de búsqueda funcionando
- [ ] Reportes y exportación
- [ ] Datos de ejemplo cargados

### Calidad
- [ ] Código comentado y documentado
- [ ] Tests unitarios pasando
- [ ] Manejo de errores apropiado
- [ ] Sin warnings o errores

### Documentación
- [ ] README.md completo
- [ ] Guía de usuario
- [ ] Documentación técnica
- [ ] Comentarios en código

### Presentación
- [ ] Demo funcionando
- [ ] Screenshots/video
- [ ] Presentación preparada
- [ ] División de trabajo clara

---

## 🆘 Contacto y Coordinación

**Repositorio**: https://github.com/olivier-gm/Gestor-de-base-de-datos-de-vulnerabilidades

**Coordinador**: [Nombre del coordinador]

**Reuniones**: [Días y horarios]

**Canal de comunicación**: WhatsApp Grupo 5

---

## 💡 Consejos para el Éxito

1. **Comunicación constante**: Avisar avances y bloqueos
2. **Commits frecuentes**: No esperar a terminar todo
3. **Ayudarse mutuamente**: Si terminas antes, ayuda a otros
4. **Testing temprano**: Probar mientras desarrollas
5. **Documentar mientras codeas**: No dejar documentación para el final

---

**¡Éxito equipo! 🚀**
