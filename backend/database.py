from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Usar una ruta absoluta para evitar problemas con rutas relativas
<<<<<<< HEAD
DATABASE_URL = "sqlite:///./database/inventario_sistema.db"
=======
DATABASE_URL = "sqlite:///C:/Users/Lenovo/Desktop/sistema-inventario/backend/database/inventario_sistema.db"
>>>>>>> fcf9aa17a154f72265472b74da8da620bf9c1c39
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

<<<<<<< HEAD

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

=======
>>>>>>> fcf9aa17a154f72265472b74da8da620bf9c1c39
if __name__ == "__main__":
    # Probar la conexión a la base de datos
    try:
        # Intentar crear la conexión
        with engine.connect() as connection:
            print("Conexión a la base de datos exitosa.")
    except Exception as e:
        print(f"Error al conectar a la base de datos: {e}")