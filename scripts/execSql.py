#!/usr/bin/env python3
"""
Script para ejecutar consultas SQL directamente en la base de datos local
Solo se puede ejecutar en entorno local por seguridad
"""
import os
import sys
from pathlib import Path

# Agregar el directorio raíz al path para imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from core.database import engine
from sqlalchemy import text
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_local_environment():
    """Verificar que estamos en entorno local"""
    # Verificar variables de entorno que indican entorno local
    if os.getenv('ENVIRONMENT') == 'production':
        logger.error("❌ Este script solo se puede ejecutar en entorno local")
        sys.exit(1)
    
    if os.getenv('DATABASE_URL') and 'localhost' not in os.getenv('DATABASE_URL', ''):
        logger.error("❌ Este script solo se puede ejecutar con base de datos local")
        sys.exit(1)
    
    logger.info("✅ Entorno local detectado")

def execute_sql(query: str):
    """Ejecutar consulta SQL"""
    try:
        with engine.connect() as connection:
            result = connection.execute(text(query))
            
            # Si es una consulta SELECT, mostrar resultados
            if query.strip().upper().startswith('SELECT'):
                rows = result.fetchall()
                if rows:
                    # Obtener nombres de columnas
                    columns = result.keys()
                    print(f"\n📊 Resultados ({len(rows)} filas):")
                    print("-" * 80)
                    
                    # Mostrar encabezados
                    header = " | ".join([f"{col:15}" for col in columns])
                    print(header)
                    print("-" * 80)
                    
                    # Mostrar datos
                    for row in rows:
                        row_str = " | ".join([f"{str(val):15}" for val in row])
                        print(row_str)
                else:
                    print("📭 No se encontraron resultados")
            else:
                print("✅ Consulta ejecutada exitosamente")
                
    except Exception as e:
        logger.error(f"❌ Error ejecutando consulta: {e}")
        sys.exit(1)

def main():
    """Función principal"""
    print("🔧 ExecSQL - Ejecutor de consultas SQL local")
    print("=" * 50)
    
    # Verificar entorno local
    check_local_environment()
    
    # Verificar argumentos
    if len(sys.argv) < 2:
        print("📝 Uso: python scripts/execSql.py \"SELECT * FROM table_name\"")
        print("📝 Ejemplo: python scripts/execSql.py \"SELECT table_name FROM information_schema.tables WHERE table_name = 'company_pages'\"")
        sys.exit(1)
    
    # Obtener consulta SQL
    query = sys.argv[1]
    
    print(f"🔍 Ejecutando consulta: {query}")
    print("-" * 50)
    
    # Ejecutar consulta
    execute_sql(query)
    
    print("\n✅ Script completado")

if __name__ == "__main__":
    main()
