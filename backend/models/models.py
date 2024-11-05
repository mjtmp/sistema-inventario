from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean, Date
from sqlalchemy.orm import relationship
from backend.database import Base  # Mantén esta importación

class Rol(Base):
    __tablename__ = "Roles"

    rol_id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, index=True)

class Usuario(Base):
    __tablename__ = "Usuarios"

    usuario_id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    contraseña = Column(String)
    rol_id = Column(Integer, ForeignKey("Roles.rol_id"))

    rol = relationship("Rol")

class Producto(Base):
    __tablename__ = "Productos"

    producto_id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    descripcion = Column(String)  # Nuevo campo 'descripcion'
    precio = Column(Float)
    tiene_iva = Column(Boolean)
    stock = Column(Integer)
    proveedor_id = Column(Integer, ForeignKey("Proveedores.proveedor_id"))  # Clave foránea a 'proveedores'

    proveedor = relationship("Proveedor", back_populates="productos")

class Proveedor(Base):
    __tablename__ = "Proveedores"

    proveedor_id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    email = Column(String, index=True)
    telefono = Column(String, index=True)
    direccion = Column(String, index=True)
    
    productos = relationship("Producto", back_populates="proveedor")  # Relación inversa

class Cliente(Base):
    __tablename__ = "Clientes"

    cliente_id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    email = Column(String, unique=True)
    telefono = Column(String)
    direccion = Column(String)
    
    # Relación con pedidos
    pedidos = relationship("Pedido", back_populates="cliente")

class Pedido(Base):
    __tablename__ = "Pedidos"

    pedido_id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("Clientes.cliente_id"))
    fecha = Column(Date)
    total = Column(Float)

    cliente = relationship("Cliente", back_populates="pedidos")
    detalles = relationship("DetallePedido", back_populates="pedido")

class DetallePedido(Base):
    __tablename__ = "DetallePedidos"

    detalle_id = Column(Integer, primary_key=True, index=True)
    pedido_id = Column(Integer, ForeignKey("Pedidos.pedido_id"))
    producto_id = Column(Integer, ForeignKey("Productos.producto_id"))
    cantidad = Column(Integer, nullable=False)
    precio_unitario = Column(Float, nullable=False)

    pedido = relationship("Pedido", back_populates="detalles")
    producto = relationship("Producto")

class ReportesEntrega(Base):
    __tablename__ = "ReportesEntrega"

    entrega_id = Column(Integer, primary_key=True, index=True)
    pedido_id = Column(Integer, ForeignKey("Pedidos.pedido_id"))
    fecha_entrega = Column(Date, nullable=False)
    estado = Column(String, nullable=False)

    pedido = relationship("Pedido")

class ReportesInventario(Base):
    __tablename__ = "ReportesInventario"

    reporte_id = Column(Integer, primary_key=True, index=True)
    fecha = Column(Date, nullable=False)
    producto_id = Column(Integer, ForeignKey("Productos.producto_id"))
    stock = Column(Integer, nullable=False)

    producto = relationship("Producto")

