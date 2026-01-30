"""
Módulo de conexión a MongoDB.
Gestiona la conexión a la base de datos usando variables de entorno.
"""

import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Variables de configuración
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
DB_NAME = os.getenv('DB_NAME', 'vulnerabilities_db')

# Cliente global de MongoDB
_client = None
_database = None


def get_database():
    """
    Obtiene la conexión a la base de datos MongoDB.

    Returns:
        Database: Instancia de la base de datos MongoDB

    Raises:
        ConnectionFailure: Si no se puede conectar a MongoDB
    """
    global _client, _database

    if _database is None:
        try:
            print(f"🔄 Conectando a MongoDB en: {MONGO_URI}")

            # Crear cliente de MongoDB con timeout
            _client = MongoClient(
                MONGO_URI,
                serverSelectionTimeoutMS=5000,  # 5 segundos timeout
                connectTimeoutMS=10000,         # 10 segundos para conectar
            )

            # Verificar conexión
            _client.admin.command('ping')

            # Obtener base de datos
            _database = _client[DB_NAME]

            print(f"✅ Conectado exitosamente a la base de datos: {DB_NAME}")

            # Crear índices para optimizar búsquedas
            _create_indexes()

        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            print(f"❌ Error al conectar a MongoDB: {e}")
            print("\n💡 Verifica que MongoDB esté ejecutándose:")
            print("   - Windows: Servicio de MongoDB activo")
            print("   - Linux/Mac: sudo systemctl start mongod")
            print("   - O usa MongoDB Atlas (nube)")
            raise
        except Exception as e:
            print(f"❌ Error inesperado: {e}")
            raise

    return _database


def _create_indexes():
    """
    Crea índices en la colección para mejorar el rendimiento de búsquedas.
    """
    try:
        collection = _database['vulnerabilities']

        # Índice único para CVE_ID
        collection.create_index('cve_id', unique=True)

        # Índice para búsquedas por severidad
        collection.create_index('severity')

        # Índice para búsquedas por fecha
        collection.create_index('published_date')

        # Índice para búsquedas por estado
        collection.create_index('status')

        print("📊 Índices de base de datos creados/verificados")

    except Exception as e:
        print(f"⚠️  Advertencia al crear índices: {e}")


def close_connection():
    """
    Cierra la conexión a MongoDB de forma segura.
    """
    global _client, _database

    if _client is not None:
        try:
            _client.close()
            _client = None
            _database = None
            print("🔒 Conexión a MongoDB cerrada correctamente")
        except Exception as e:
            print(f"⚠️  Error al cerrar conexión: {e}")


def test_connection():
    """
    Prueba la conexión a MongoDB y muestra información del servidor.

    Returns:
        bool: True si la conexión es exitosa, False en caso contrario
    """
    try:
        db = get_database()

        # Obtener información del servidor
        server_info = _client.server_info()

        print("\n📡 Información del servidor MongoDB:")
        print(f"   Versión: {server_info.get('version', 'Desconocida')}")
        print(f"   Base de datos: {DB_NAME}")

        # Listar colecciones
        collections = db.list_collection_names()
        print(f"   Colecciones: {collections if collections else 'Ninguna (nueva base de datos)'}")

        # Contar documentos
        if 'vulnerabilities' in collections:
            count = db['vulnerabilities'].count_documents({})
            print(f"   Vulnerabilidades registradas: {count}")

        return True

    except Exception as e:
        print(f"\n❌ Error en prueba de conexión: {e}")
        return False


# Ejecutar si se ejecuta directamente este archivo
if __name__ == "__main__":
    print("🔍 Probando conexión a MongoDB...\n")

    if test_connection():
        print("\n✅ Prueba de conexión exitosa!")
    else:
        print("\n❌ Prueba de conexión fallida")

    close_connection()
