from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Usar una ruta absoluta para evitar problemas con rutas relativas
DATABASE_URL = "sqlite:///C:/Users/Lenovo/Desktop/sistema-inventario/backend/database/inventario_sistema.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

if __name__ == "__main__":
    # Probar la conexión a la base de datos
    try:
        # Intentar crear la conexión
        with engine.connect() as connection:
            print("Conexión a la base de datos exitosa.")
    except Exception as e:
        print(f"Error al conectar a la base de datos: {e}")