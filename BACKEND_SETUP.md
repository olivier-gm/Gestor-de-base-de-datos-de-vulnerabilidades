# 🔧 Backend & Base de Datos - Guía del Integrante 1

## 📌 Tu Responsabilidad

Eres responsable de la **capa de datos** del proyecto. Has implementado:

1. **Conexión a MongoDB** (`database/connection.py`)
2. **Modelo de datos** (`database/models.py`)
3. **Configuración del proyecto** (`requirements.txt`, `.env`, `.gitignore`)

## 📁 Archivos Creados

```
TeI-project/
├── database/
│   ├── __init__.py          ✅ Módulo de base de datos
│   ├── connection.py        ✅ Conexión a MongoDB
│   └── models.py            ✅ Modelo de vulnerabilidades
├── requirements.txt         ✅ Dependencias
├── .gitignore              ✅ Archivos a ignorar
└── .env.example            ✅ Plantilla de configuración
```

## 🚀 Instalación y Configuración

### 1. Instalar MongoDB

**Opción A: MongoDB Local (Recomendado para desarrollo)**

**Windows:**
```bash
# Descargar desde:
https://www.mongodb.com/try/download/community

# Instalar y verificar
mongod --version
```

**Linux (Ubuntu/Debian):**
```bash
# Importar clave GPG
wget -qO - https://www.mongodb.org/static/pgp/server-7.0.asc | sudo apt-key add -

# Agregar repositorio
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/7.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-7.0.list

# Instalar
sudo apt-get update
sudo apt-get install -y mongodb-org

# Iniciar servicio
sudo systemctl start mongod
sudo systemctl enable mongod

# Verificar
sudo systemctl status mongod
```

**macOS:**
```bash
# Usando Homebrew
brew tap mongodb/brew
brew install mongodb-community

# Iniciar servicio
brew services start mongodb-community

# Verificar
brew services list
```

**Opción B: MongoDB Atlas (Nube - Gratis)**
1. Registrarse en: https://www.mongodb.com/cloud/atlas/register
2. Crear cluster gratuito (M0)
3. Crear usuario de base de datos
4. Whitelist IP (0.0.0.0/0 para desarrollo)
5. Obtener connection string

### 2. Configurar Variables de Entorno

```bash
# Copiar plantilla
cp .env.example .env

# Editar .env con tu configuración
nano .env  # o usa tu editor preferido
```

**Para MongoDB Local:**
```env
MONGO_URI=mongodb://localhost:27017/
DB_NAME=vulnerabilities_db
APP_ENV=development
LOG_LEVEL=INFO
```

**Para MongoDB Atlas:**
```env
MONGO_URI=mongodb+srv://usuario:password@cluster.mongodb.net/
DB_NAME=vulnerabilities_db
APP_ENV=development
LOG_LEVEL=INFO
```

### 3. Instalar Dependencias de Python

```bash
# Crear entorno virtual (recomendado)
python -m venv venv

# Activar entorno virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

## ✅ Probar tu Implementación

### Prueba 1: Conexión a MongoDB

```bash
python database/connection.py
```

**Salida esperada:**
```
🔍 Probando conexión a MongoDB...

🔄 Conectando a MongoDB en: mongodb://localhost:27017/
✅ Conectado exitosamente a la base de datos: vulnerabilities_db
📊 Índices de base de datos creados/verificados

📡 Información del servidor MongoDB:
   Versión: 7.0.x
   Base de datos: vulnerabilities_db
   Colecciones: Ninguna (nueva base de datos)

✅ Prueba de conexión exitosa!
🔒 Conexión a MongoDB cerrada correctamente
```

### Prueba 2: Modelo de Datos

```bash
python database/models.py
```

**Salida esperada:**
```
🔍 Probando modelo de vulnerabilidades...

✅ Modelo validado correctamente

======================================================================
🆔 CVE ID: CVE-2025-00001
📌 Título: Buffer Overflow en Apache HTTP Server
======================================================================

📄 Descripción:
   Vulnerabilidad de desbordamiento de búfer en módulo mod_proxy

🔴 Severidad: Critical
📊 CVSS Score: 9.8/10.0

💻 Sistemas Afectados:
   • Apache HTTP Server 2.4.x
   • Apache HTTP Server 2.5.0

📅 Publicado: 2025-01-30
🔄 Última modificación: 2025-01-30
🔓 Estado: Open

🔗 Referencias:
   • https://nvd.nist.gov/vuln/detail/CVE-2025-00001

🛡️  Mitigación:
   Actualizar a versión 2.4.58 o superior
======================================================================
```

## 🧪 Pruebas Adicionales

### Probar Conexión desde Python Interactivo

```python
python

>>> from database.connection import get_database, test_connection
>>>
>>> # Probar conexión
>>> test_connection()
>>>
>>> # Obtener base de datos
>>> db = get_database()
>>>
>>> # Verificar colecciones
>>> print(db.list_collection_names())
>>>
>>> # Cerrar conexión
>>> from database.connection import close_connection
>>> close_connection()
```

### Probar Validación de Modelo

```python
python

>>> from database.models import VulnerabilityModel, validate_vulnerability
>>>
>>> # Datos de prueba
>>> test_data = {
...     'cve_id': 'CVE-2025-TEST',
...     'title': 'Vulnerabilidad de Prueba',
...     'description': 'Esta es una prueba',
...     'severity': 'High',
...     'cvss_score': 8.5,
...     'affected_systems': ['Sistema Test 1.0']
... }
>>>
>>> # Validar
>>> is_valid, error = validate_vulnerability(test_data)
>>> print(f"¿Válido?: {is_valid}")
>>> print(f"Error: {error}")
>>>
>>> # Crear instancia
>>> vuln = VulnerabilityModel(test_data)
>>> print(vuln.to_display())
```

## 🐛 Solución de Problemas

### Error: "No module named 'pymongo'"
```bash
pip install pymongo
```

### Error: "No module named 'dotenv'"
```bash
pip install python-dotenv
```

### Error: "ConnectionFailure" o "ServerSelectionTimeoutError"
- Verifica que MongoDB esté ejecutándose:
  ```bash
  # Linux
  sudo systemctl status mongod

  # Windows (en Servicios)
  services.msc  # Busca "MongoDB"

  # Mac
  brew services list
  ```
- Verifica el MONGO_URI en tu `.env`
- Para MongoDB Atlas, verifica tu IP en Network Access

### Error: "Authentication failed"
- Verifica usuario y password en MONGO_URI
- Para Atlas, verifica que el usuario esté creado en Database Access

### MongoDB no inicia (Linux)
```bash
# Ver logs
sudo journalctl -u mongod

# Reiniciar servicio
sudo systemctl restart mongod
```

## 📚 Conceptos Importantes

### 1. PyMongo
Driver oficial de MongoDB para Python. Permite:
- Conectar a bases de datos MongoDB
- Realizar operaciones CRUD
- Crear índices y optimizar búsquedas

### 2. Variables de Entorno (.env)
- Almacenan configuración sensible (URIs, passwords)
- **NUNCA** se suben a Git
- Cada desarrollador tiene su propio `.env`

### 3. Modelo de Datos
- Define estructura de vulnerabilidades
- Valida datos antes de guardar en BD
- Previene datos inconsistentes

### 4. Índices MongoDB
Mejoran rendimiento de búsquedas:
- `cve_id`: Índice único (previene duplicados)
- `severity`: Búsquedas rápidas por severidad
- `published_date`: Búsquedas por fecha
- `status`: Filtros por estado

## 🔄 Integración con Otros Módulos

### Para Integrante 2 (CRUD):
```python
from database.connection import get_database
from database.models import VulnerabilityModel

# Obtener base de datos
db = get_database()
collection = db['vulnerabilities']

# Ejemplo: Insertar vulnerabilidad
vuln_data = {...}
vuln = VulnerabilityModel(vuln_data)
collection.insert_one(vuln.to_dict())
```

### Para Integrante 3 (UI/Utils):
```python
from database.connection import get_database
from database.models import VulnerabilityModel

# Mostrar vulnerabilidad
vuln = VulnerabilityModel(data)
print(vuln.to_display())
```

## 📖 Recursos de Estudio

### MongoDB
- [MongoDB Manual](https://www.mongodb.com/docs/manual/)
- [PyMongo Documentation](https://pymongo.readthedocs.io/)
- [MongoDB University (Gratis)](https://university.mongodb.com/)

### Python Best Practices
- [PEP 8 – Style Guide](https://pep8.org/)
- [Python Docs](https://docs.python.org/3/)

### CVE y Vulnerabilidades
- [CVE Program](https://cve.mitre.org/)
- [NIST NVD](https://nvd.nist.gov/)
- [CVSS Calculator](https://www.first.org/cvss/calculator/3.1)

## ✅ Checklist de Completitud

- [x] Instalado MongoDB (local o Atlas)
- [x] Creado archivo `.env` con configuración
- [x] Instaladas dependencias Python (`pip install -r requirements.txt`)
- [x] Probado `python database/connection.py` exitosamente
- [x] Probado `python database/models.py` exitosamente
- [x] Documentación leída y comprendida
- [ ] Coordinado con Integrante 2 para integración CRUD
- [ ] Realizado commit y push al repositorio

## 🤝 Coordinación con Equipo

### Información para compartir:

**Para Integrante 2 (CRUD):**
```python
# Conexión a usar
from database.connection import get_database
db = get_database()
collection = db['vulnerabilities']

# Modelo a usar
from database.models import VulnerabilityModel
vuln = VulnerabilityModel(data)
```

**Para Integrante 3 (UI):**
```python
# Para mostrar vulnerabilidades
from database.models import VulnerabilityModel
print(vuln.to_display())

# Severidades válidas
VulnerabilityModel.VALID_SEVERITIES  # ['Critical', 'High', 'Medium', 'Low']

# Estados válidos
VulnerabilityModel.VALID_STATUSES    # ['Open', 'Patched', 'Investigating']
```

**Para Integrante 4 (Testing):**
```python
# Función de validación
from database.models import validate_vulnerability
is_valid, error = validate_vulnerability(data)

# Estadísticas
from database.models import get_collection_stats
stats = get_collection_stats(db)
```

## 💡 Próximos Pasos

1. Completar pruebas de conexión
2. Coordinar con Integrante 2 sobre estructura de colección
3. Documentar cualquier cambio en configuración
4. Estar disponible para resolver dudas de conexión DB

---

**🎯 Tu rol es fundamental: sin una base de datos funcionando, el resto del equipo no puede trabajar. ¡Eres la base del proyecto!**
