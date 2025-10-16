#!/usr/bin/env python3
"""
Migración para agregar constraint único al campo email en la tabla candidates
"""
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def run_migration():
    """Ejecuta la migración para agregar el constraint único"""
    
    # Obtener la URL de la base de datos
    database_url = os.getenv("DATABASE_URL", "sqlite:///./test.db")
    
    # Crear engine
    engine = create_engine(database_url)
    
    try:
        with engine.connect() as conn:
            # Para SQLite, necesitamos recrear la tabla con el constraint
            if "sqlite" in database_url.lower():
                print("Detectada base de datos SQLite, aplicando migración...")
                
                # Verificar si ya existe el constraint
                result = conn.execute(text("PRAGMA table_info(candidates)"))
                columns = result.fetchall()
                
                # Buscar si el email ya tiene constraint único
                email_column = None
                for col in columns:
                    if col[1] == 'email':  # col[1] es el nombre de la columna
                        email_column = col
                        break
                
                if email_column:
                    print("Campo email encontrado, verificando constraint único...")
                    
                    # Para SQLite, verificamos los índices únicos
                    result = conn.execute(text("PRAGMA index_list(candidates)"))
                    indexes = result.fetchall()
                    
                    email_unique_exists = False
                    for idx in indexes:
                        if idx[2] == 1:  # idx[2] indica si es único
                            # Verificar si el índice es para email
                            result = conn.execute(text(f"PRAGMA index_info({idx[1]})"))
                            index_info = result.fetchall()
                            for info in index_info:
                                if info[2] == 'email':  # info[2] es el nombre de la columna
                                    email_unique_exists = True
                                    break
                    
                    if not email_unique_exists:
                        print("Agregando constraint único al campo email...")
                        
                        # Para SQLite, necesitamos crear un índice único
                        conn.execute(text("CREATE UNIQUE INDEX IF NOT EXISTS idx_candidates_email_unique ON candidates(email)"))
                        conn.commit()
                        print("Constraint único agregado exitosamente!")
                    else:
                        print("El constraint único ya existe en el campo email.")
                else:
                    print("Campo email no encontrado en la tabla candidates.")
            
            else:
                # Para PostgreSQL/MySQL
                print("Detectada base de datos PostgreSQL/MySQL, aplicando migración...")
                
                # Verificar si el constraint ya existe
                if "postgresql" in database_url.lower():
                    result = conn.execute(text("""
                        SELECT constraint_name 
                        FROM information_schema.table_constraints 
                        WHERE table_name = 'candidates' 
                        AND constraint_type = 'UNIQUE'
                        AND constraint_name LIKE '%email%'
                    """))
                else:  # MySQL
                    result = conn.execute(text("""
                        SELECT CONSTRAINT_NAME 
                        FROM information_schema.TABLE_CONSTRAINTS 
                        WHERE TABLE_NAME = 'candidates' 
                        AND CONSTRAINT_TYPE = 'UNIQUE'
                        AND CONSTRAINT_NAME LIKE '%email%'
                    """))
                
                existing_constraints = result.fetchall()
                
                if not existing_constraints:
                    print("Agregando constraint único al campo email...")
                    conn.execute(text("ALTER TABLE candidates ADD CONSTRAINT uq_candidates_email UNIQUE (email)"))
                    conn.commit()
                    print("Constraint único agregado exitosamente!")
                else:
                    print("El constraint único ya existe en el campo email.")
                    
    except Exception as e:
        print(f"Error durante la migración: {e}")
        raise

if __name__ == "__main__":
    run_migration()