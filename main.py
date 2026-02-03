
"""
Punto de entrada de la aplicación.
"""
import sys
from database.connection import get_database, close_connection
from ui.menu import main_loop

if __name__ == "__main__":
    try:
        print("🔐 Gestor de Vulnerabilidades - Iniciando...")
        db = get_database()
        if db is not None:
            main_loop(db)
        else:
            print("❌ No se pudo establecer conexión con la base de datos.")
    except KeyboardInterrupt:
        print("\n\n👋 Saliendo...")
    except Exception as e:
        print(f"❌ Error crítico: {e}")
    finally:
        close_connection()
        print("✅ Aplicación cerrada")
        sys.exit(0)
