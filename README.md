# 🔐 Gestor de Base de Datos de Vulnerabilidades

> Repositorio de conocimiento en ciberseguridad - Mini SOC Knowledge Base

## 📋 Descripción

Sistema de gestión de vulnerabilidades tipo CVE desarrollado en Python con MongoDB. Permite organizar, consultar y administrar información técnica sobre vulnerabilidades de seguridad de forma estructurada.

## 🎯 Objetivo

Crear un repositorio de conocimiento para equipos SOC (Security Operations Center) que facilite la organización y consulta de vulnerabilidades, similar a bases de datos profesionales como NVD (National Vulnerability Database).

## ✨ Funcionalidades

### CRUD Completo
- **Create**: Registrar nuevas vulnerabilidades con información detallada
- **Read**: Consultar vulnerabilidades por ID, severidad o afectados
- **Update**: Actualizar información de vulnerabilidades existentes
- **Delete**: Eliminar registros de vulnerabilidades

### Características Adicionales
- Generación automática de IDs tipo CVE (CVE-2025-XXXXX)
- Clasificación por severidad (Critical, High, Medium, Low)
- Sistema de búsqueda y filtros
- Reportes y estadísticas
- Exportación de datos

## 🛠️ Tecnologías

- **Lenguaje**: Python 3.8+
- **Base de Datos**: MongoDB
- **Librerías principales**:
  - `pymongo`: Conexión con MongoDB
  - `python-dotenv`: Gestión de variables de entorno
  - `datetime`: Manejo de fechas

## 📦 Instalación

### Prerrequisitos

1. **Python 3.8 o superior**
   ```bash
   python --version
   ```

2. **MongoDB instalado y ejecutándose**
   - [Descargar MongoDB Community](https://www.mongodb.com/try/download/community)
   - O usar MongoDB Atlas (nube gratuita)

### Pasos de Instalación

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/olivier-gm/Gestor-de-base-de-datos-de-vulnerabilidades.git
   cd Gestor-de-base-de-datos-de-vulnerabilidades
   ```

2. **Crear entorno virtual** (recomendado)
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar variables de entorno**
   
   Crear archivo `.env` en la raíz del proyecto:
   ```env
   MONGO_URI=mongodb://localhost:27017/
   DB_NAME=vulnerabilities_db
   ```

5. **Ejecutar la aplicación**
   ```bash
   python main.py
   ```

## 📊 Estructura del Proyecto

```
Gestor-de-base-de-datos-de-vulnerabilidades/
│
├── main.py                 # Punto de entrada de la aplicación
├── requirements.txt        # Dependencias del proyecto
├── .env                    # Variables de entorno (no incluir en git)
├── .gitignore             # Archivos a ignorar por git
├── README.md              # Este archivo
│
├── database/
│   ├── __init__.py
│   ├── connection.py      # Conexión a MongoDB
│   └── models.py          # Modelos de datos
│
├── crud/
│   ├── __init__.py
│   ├── create.py          # Crear vulnerabilidades
│   ├── read.py            # Leer/Consultar vulnerabilidades
│   ├── update.py          # Actualizar vulnerabilidades
│   └── delete.py          # Eliminar vulnerabilidades
│
├── utils/
│   ├── __init__.py
│   ├── validators.py      # Validación de datos
│   ├── generators.py      # Generador de IDs CVE
│   └── reports.py         # Generación de reportes
│
├── ui/
│   ├── __init__.py
│   └── menu.py            # Interfaz de usuario (consola)
│
└── tests/
    ├── __init__.py
    └── sample_data.py     # Datos de ejemplo para pruebas
```

## 💾 Modelo de Datos

Cada vulnerabilidad se almacena con la siguiente estructura:

```json
{
  "cve_id": "CVE-2025-00001",
  "title": "Buffer Overflow in Apache HTTP Server",
  "description": "Descripción detallada de la vulnerabilidad",
  "severity": "Critical",
  "cvss_score": 9.8,
  "affected_systems": ["Apache HTTP Server 2.4.x"],
  "published_date": "2025-01-29",
  "last_modified": "2025-01-29",
  "status": "Open",
  "references": [
    "https://nvd.nist.gov/vuln/detail/CVE-2025-00001"
  ],
  "mitigation": "Actualizar a versión 2.4.58 o superior"
}
```

### Campos del Modelo

- **cve_id**: Identificador único tipo CVE
- **title**: Título breve de la vulnerabilidad
- **description**: Descripción técnica detallada
- **severity**: Nivel de severidad (Critical/High/Medium/Low)
- **cvss_score**: Puntuación CVSS (0.0 - 10.0)
- **affected_systems**: Lista de sistemas afectados
- **published_date**: Fecha de publicación
- **last_modified**: Última fecha de modificación
- **status**: Estado (Open/Patched/Investigating)
- **references**: URLs de referencia
- **mitigation**: Medidas de mitigación recomendadas

## 🚀 Uso

### Menú Principal

```
=== GESTOR DE VULNERABILIDADES ===
1. Registrar nueva vulnerabilidad
2. Consultar vulnerabilidad
3. Listar todas las vulnerabilidades
4. Buscar por severidad
5. Actualizar vulnerabilidad
6. Eliminar vulnerabilidad
7. Generar reporte
8. Salir
```

### Ejemplos de Uso

**Registrar una vulnerabilidad**:
```python
# Se solicita al usuario ingresar:
# - Título
# - Descripción
# - Severidad
# - Sistemas afectados
# El sistema genera automáticamente el CVE-ID
```

**Buscar por severidad**:
```python
# Filtrar vulnerabilidades críticas
# Muestra todas las vulnerabilidades con severidad "Critical"
```

## 👥 Equipo de Desarrollo

- **Integrante 1**: Backend & Base de Datos
- **Integrante 2**: Interfaz de Usuario
- **Integrante 3**: Lógica de Negocio
- **Integrante 4**: Documentación & Testing

## 📝 Tareas Pendientes

- [ ] Configurar conexión a MongoDB
- [ ] Implementar operaciones CRUD
- [ ] Crear interfaz de usuario
- [ ] Desarrollar sistema de reportes
- [ ] Escribir pruebas unitarias
- [ ] Agregar datos de ejemplo
- [ ] Documentar código

## 🔄 Flujo de Trabajo Git

```bash
# Crear rama para tu tarea
git checkout -b feature/nombre-funcionalidad

# Hacer cambios y commits
git add .
git commit -m "Descripción clara del cambio"

# Subir cambios
git push origin feature/nombre-funcionalidad

# Crear Pull Request en GitHub para revisión
```

## 📚 Recursos Adicionales

- [CVE - Common Vulnerabilities and Exposures](https://cve.mitre.org/)
- [NVD - National Vulnerability Database](https://nvd.nist.gov/)
- [CVSS - Common Vulnerability Scoring System](https://www.first.org/cvss/)
- [MongoDB Python Documentation](https://pymongo.readthedocs.io/)

## 📄 Licencia

Este proyecto es de uso académico para la materia de Ciberseguridad.

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:
1. Haz fork del proyecto
2. Crea una rama para tu funcionalidad
3. Haz commit de tus cambios
4. Push a la rama
5. Abre un Pull Request

---

**Desarrollado con 💙 por el Grupo 5 - Estudiantes de Ingeniería de Sistemas**
