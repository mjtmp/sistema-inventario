from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean, Date, DateTime
from sqlalchemy.orm import relationship
from database import Base
import datetime

class Rol(Base):
    __tablename__ = "Roles"

    rol_id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, index=True)
    
    usuarios = relationship("Usuario", back_populates="rol")  # Relación inversa
    permisos = relationship("Permiso", secondary="Roles_Permisos", back_populates="roles")

class Permiso(Base):
    __tablename__ = "Permisos"

    permiso_id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, index=True)
    
    roles = relationship("Rol", secondary="Roles_Permisos", back_populates="permisos")

class RolesPermisos(Base):
    __tablename__ = "Roles_Permisos"

    rol_id = Column(Integer, ForeignKey("Roles.rol_id"), primary_key=True)
    permiso_id = Column(Integer, ForeignKey("Permisos.permiso_id"), primary_key=True)

class Usuario(Base):
    __tablename__ = "Usuarios"

    usuario_id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    contraseña = Column(String)
    rol_id = Column(Integer, ForeignKey("Roles.rol_id"))
    
    # Campos de auditoría
    fecha_creacion = Column(Date, default=datetime.date.today)
    fecha_actualizacion = Column(Date, default=datetime.date.today)

    rol = relationship("Rol", back_populates="usuarios")
    facturas = relationship("Factura", back_populates="usuario")
    salidas = relationship("SalidasInventario", back_populates="vendedor")
    pedidossalidas = relationship("PedidosSalidasInventario", back_populates="vendedor")
    historial = relationship("Historial", back_populates="usuario")
    def to_dict(self):
        return {
            "usuario_id": self.usuario_id,
            "nombre": self.nombre,
            "email": self.email,
            "contraseña": self.contraseña,
            "rol_id": self.rol_id,
            "fecha_creacion": self.fecha_creacion.isoformat() if self.fecha_creacion else None,  # Formato ISO para fecha
            "fecha_actualizacion": self.fecha_actualizacion.isoformat() if self.fecha_actualizacion else None, # Formato ISO para fecha
        }

class Categoria(Base):
    __tablename__ = "Categorias"
    categoria_id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)

    productos = relationship("Producto", back_populates="categoria")

    def to_dict(self):
        return {
            "categoria_id": self.categoria_id,
            "nombre": self.nombre
        }

class Producto(Base):
    __tablename__ = "Productos"

    producto_id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    descripcion = Column(String)
    precio = Column(Float)
    tiene_iva = Column(Boolean)
    stock = Column(Integer)
    codigo = Column(String, unique=True, nullable=True)
    proveedor_id = Column(Integer, ForeignKey("Proveedores.proveedor_id"))
    ubicacion = Column(String, nullable=True) # Nuevo campo 
    cantidad_minima = Column(Integer, nullable=True) # Nuevo campo 
    cantidad_maxima = Column(Integer, nullable=True) # Nuevo Campo
    codigo_barras = Column(String, nullable=True)
    categoria_id = Column(Integer, ForeignKey("Categorias.categoria_id"))
    categoria = relationship("Categoria", back_populates="productos")

    # Relación con EntradasInventario
    entradas_inventario = relationship("EntradaInventario", back_populates="producto", cascade="all, delete-orphan")

    # Relación con la tabla Factura (si la relación es muchos a muchos)
    facturas = relationship("FacturaProducto", back_populates="producto")

    # Campos de auditoría
    fecha_creacion = Column(Date, default=datetime.date.today)
    fecha_actualizacion = Column(Date, default=datetime.date.today)

    proveedor = relationship("Proveedor", back_populates="productos")
    salidas_inventario = relationship("SalidasInventario", back_populates="producto")
    reportes_inventario = relationship("ReportesInventario", back_populates="producto")
    detallepedidos = relationship("DetallePedido", back_populates="producto") # Añadir esta relación
    detalleordenescompra = relationship("DetalleOrdenCompra", back_populates="producto")
    pedidossalidas = relationship("PedidosSalidasInventario", back_populates="producto")
    
    def to_dict(self):
        return {
            "producto_id": self.producto_id,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "precio": self.precio,
            "tiene_iva": self.tiene_iva,
            "stock": self.stock,
            "codigo": self.codigo,
            "ubicacion": self.ubicacion,
            "cantidad_minima": self.cantidad_minima,
            "cantidad_maxima": self.cantidad_maxima,
            "proveedor_id": self.proveedor_id,
            "codigo_barras": self.codigo_barras,
            "categoria_id": self.categoria_id,
            "fecha_creacion": self.fecha_creacion if isinstance(self.fecha_creacion, str) else self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            "fecha_actualizacion": self.fecha_actualizacion if isinstance(self.fecha_actualizacion, str) else self.fecha_actualizacion.isoformat() if self.fecha_actualizacion else None,
            "categoria": self.categoria.to_dict() if self.categoria else None
        }

class Proveedor(Base):
    __tablename__ = "Proveedores"

    proveedor_id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    email = Column(String, index=True)
    telefono = Column(String, index=True)
    direccion = Column(String, index=True)
    rif = Column(String)  # Nuevo campo para el RIF

    # Relación con EntradasInventario
    entradas_inventario = relationship("EntradaInventario", back_populates="proveedor")
    productos = relationship("Producto", back_populates="proveedor")
    ordenes_compra = relationship("OrdenCompra", back_populates="proveedor")

    fecha_creacion = Column(Date, default=datetime.date.today)
    fecha_actualizacion = Column(Date, default=datetime.date.today)

    # Método para convertir a diccionario
    def to_dict(self):
        return {
            "proveedor_id": self.proveedor_id,
            "nombre": self.nombre,
            "email": self.email,
            "telefono": self.telefono,
            "direccion": self.direccion,
            "rif": self.rif,
            "fecha_creacion": self.fecha_creacion if isinstance(self.fecha_creacion, str) else self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            "fecha_actualizacion": self.fecha_actualizacion if isinstance(self.fecha_actualizacion, str) else self.fecha_actualizacion.isoformat() if self.fecha_actualizacion else None,
            "productos": [producto.to_dict() for producto in self.productos]  # Convertir productos a diccionario
        }

class Cliente(Base):
    __tablename__ = "Clientes"

    cliente_id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    email = Column(String, unique=True)
    telefono = Column(String)
    direccion = Column(String)
    tipo_documento = Column(String)  # Nuevo campo para tipo de documento
    numero_documento = Column(String)  # Nuevo campo para número de documento
    
    fecha_creacion = Column(Date, default=datetime.date.today)
    fecha_actualizacion = Column(Date, default=datetime.date.today)
    
    pedidos = relationship("Pedido", back_populates="cliente")
    facturas = relationship("Factura", back_populates="cliente")  # Relación con Factura
    salidas = relationship("SalidasInventario", back_populates="cliente")
    
    facturas = relationship("Factura", back_populates="cliente")
    pedidossalidas = relationship("PedidosSalidasInventario", back_populates="cliente")
    
    def to_dict(self):
        return {
            "cliente_id": self.cliente_id,
            "nombre": self.nombre,
            "email": self.email,
            "telefono": self.telefono,
            "direccion": self.direccion,
            "tipo_documento": self.tipo_documento,  # Agregado al método to_dict
            "numero_documento": self.numero_documento,  # Agregado al método to_dict
            "fecha_creacion": self.fecha_creacion.isoformat() if self.fecha_creacion else None,  # Formato ISO para fecha
            "fecha_actualizacion": self.fecha_actualizacion.isoformat() if self.fecha_actualizacion else None, # Formato ISO para fecha
        }

class Pago(Base):
    __tablename__ = "Pagos"

    pago_id = Column(Integer, primary_key=True, index=True)
    pedido_id = Column(Integer, ForeignKey("Pedidos.pedido_id"), nullable=False)
    fecha = Column(Date, default=datetime.date.today)
    monto = Column(Float, nullable=False)
    metodo_pago = Column(String)

    pedido = relationship("Pedido", back_populates="pagos")

class Factura(Base):
    __tablename__ = "Facturas"

    factura_id = Column(Integer, primary_key=True, index=True)
    pedido_id = Column(Integer, ForeignKey("Pedidos.pedido_id"), nullable=False)
    usuario_id = Column(Integer, ForeignKey("Usuarios.usuario_id"), nullable=False)
    cliente_id = Column(Integer, ForeignKey("Clientes.cliente_id"), nullable=False)
    numero_factura = Column(String, unique=True, nullable=False)
    fecha_emision = Column(Date, default=datetime.date.today)
    monto_total = Column(Float, nullable=False)
    pagado = Column(Float, default=0.0) # Asegúrate de incluir este campo 
    debido = Column(Float, default=0.0) # Asegúrate de incluir este campo
    estado = Column(String, default='pendiente')  # Estado de la factura (pendiente, pagada, etc.)

    # Relación con Pedido
    pedido = relationship("Pedido", back_populates="factura")
    # Relación con los productos de la factura (a través de la tabla intermedia)
    productos = relationship("FacturaProducto", back_populates="factura")
    usuario = relationship("Usuario", back_populates="facturas")
    cliente = relationship("Cliente", back_populates="facturas")
    # Relación con SalidasInventario 
    salidas = relationship("SalidasInventario", back_populates="factura")

    def to_dict(self):
        return {
            "factura_id": self.factura_id,
            "pedido_id": self.pedido_id,
            "usuario_id": self.usuario_id,
            "cliente_id": self.cliente_id,
            "numero_factura": self.numero_factura,
            "fecha_emision": self.fecha_emision.isoformat() if self.fecha_emision else None,
            "monto_total": self.monto_total,
            "estado": self.estado,
            # Puedes incluir los productos a través de SalidasInventario
            "productos": [fp.producto.to_dict() for fp in self.productos]

        }   

class FacturaProducto(Base):
    __tablename__ = "FacturaProductos"
    id = Column(Integer, primary_key=True, index=True)
    factura_id = Column(Integer, ForeignKey("Facturas.factura_id"))
    producto_id = Column(Integer, ForeignKey("Productos.producto_id"))
    cantidad = Column(Integer, nullable=False)
    precio_unitario = Column(Float, nullable=False)
    factura = relationship("Factura", back_populates="productos")
    producto = relationship("Producto", back_populates="facturas")
    
    def monto_total(self): return self.cantidad * self.precio_unitario

class Pedido(Base):
    __tablename__ = "Pedidos"

    pedido_id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("Clientes.cliente_id"), nullable=False)
    fecha_pedido = Column(Date, default=datetime.date.today)
    estado = Column(String, default='pendiente')

    # Relación con Cliente
    cliente = relationship("Cliente", back_populates="pedidos")
    detalles = relationship("DetallePedido", back_populates="pedido", cascade="all, delete-orphan")
    entregas = relationship("ReportesEntrega", back_populates="pedido")
    pagos = relationship("Pago", back_populates="pedido")

    # Relación con Factura
    factura = relationship("Factura", back_populates="pedido", uselist=False)
   #salida = relationship("SalidasInventario", back_populates="pedido")
    pedidossalidas = relationship("PedidosSalidasInventario", back_populates="pedido")

    def to_dict(self):
        return {
            "pedido_id": self.pedido_id,
            "cliente_id": self.cliente_id,
            "fecha_pedido": self.fecha_pedido.isoformat() if self.fecha_pedido else None,
            "estado": self.estado,
        }

class DetallePedido(Base):
    __tablename__ = "DetallePedidos"

    detalle_id = Column(Integer, primary_key=True, index=True)
    pedido_id = Column(Integer, ForeignKey("Pedidos.pedido_id"))
    producto_id = Column(Integer, ForeignKey("Productos.producto_id"))
    cantidad = Column(Integer, nullable=False)
    precio_unitario = Column(Float, nullable=False)

    pedido = relationship("Pedido", back_populates="detalles")
    producto = relationship("Producto", back_populates="detallepedidos")

    def to_dict(self):
        return {
            "detalle_id": self.detalle_id,
            "pedido_id": self.pedido_id,
            "producto_id": self.producto_id,
            "cantidad": self.cantidad,
            "precio_unitario": self.precio_unitario
        }

class OrdenCompra(Base):
    __tablename__ = "OrdenesCompra"

    orden_compra_id = Column(Integer, primary_key=True, index=True)
    proveedor_id = Column(Integer, ForeignKey("Proveedores.proveedor_id"), nullable=False)
    fecha_orden = Column(Date, default=datetime.date.today)
    estado = Column(String, default='pendiente')

    proveedor = relationship("Proveedor", back_populates="ordenes_compra")
    detalles = relationship("DetalleOrdenCompra", back_populates="orden_compra", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "orden_compra_id": self.orden_compra_id,
            "proveedor_id": self.proveedor_id,
            "fecha_orden": self.fecha_orden.isoformat() if self.fecha_orden else None,
            "estado": self.estado,
            "detalles": [detalle.to_dict() for detalle in self.detalles]
        }

class DetalleOrdenCompra(Base):
    __tablename__ = "DetalleOrdenesCompra"

    detalle_id = Column(Integer, primary_key=True, index=True)
    orden_compra_id = Column(Integer, ForeignKey("OrdenesCompra.orden_compra_id"))
    producto_id = Column(Integer, ForeignKey("Productos.producto_id"))
    cantidad = Column(Integer, nullable=False)
    precio_unitario = Column(Float, nullable=False)

    orden_compra = relationship("OrdenCompra", back_populates="detalles")
    producto = relationship("Producto", back_populates="detalleordenescompra")

    def to_dict(self):
        return {
            "detalle_id": self.detalle_id,
            "orden_compra_id": self.orden_compra_id,
            "producto_id": self.producto_id,
            "cantidad": self.cantidad,
            "precio_unitario": self.precio_unitario
        }

class ReportesEntrega(Base):
    __tablename__ = "ReportesEntrega"

    entrega_id = Column(Integer, primary_key=True, index=True)
    pedido_id = Column(Integer, ForeignKey("Pedidos.pedido_id"))
    fecha_entrega = Column(Date, nullable=False)
    estado = Column(String, nullable=False)

    pedido = relationship("Pedido", back_populates="entregas")

class ReportesInventario(Base):
    __tablename__ = "ReportesInventario"

    reporte_id = Column(Integer, primary_key=True, index=True)
    fecha = Column(Date, nullable=False)
    producto_id = Column(Integer, ForeignKey("Productos.producto_id"))
    stock = Column(Integer, nullable=False)

    producto = relationship("Producto", back_populates="reportes_inventario")
    
class EntradaInventario(Base):
    __tablename__ = "EntradasInventario"
    entrada_id = Column(Integer, primary_key=True, index=True)
    producto_id = Column(Integer, ForeignKey("Productos.producto_id"))
    cantidad = Column(Integer, nullable=False)
    precio_compra = Column(Float, nullable=False)
    fecha = Column(Date, default=datetime.date.today)
    proveedor_id = Column(Integer, ForeignKey("Proveedores.proveedor_id"))

    producto = relationship("Producto", back_populates="entradas_inventario")
    proveedor = relationship("Proveedor", back_populates="entradas_inventario")

class SalidasInventario(Base):
    __tablename__ = "SalidasInventario"

    salida_id = Column(Integer, primary_key=True, index=True)
    producto_id = Column(Integer, ForeignKey("Productos.producto_id"))
    cliente_id = Column(Integer, ForeignKey("Clientes.cliente_id"))
    factura_id = Column(Integer, ForeignKey("Facturas.factura_id"), nullable=False)
    cantidad = Column(Integer, nullable=False)
    precio_venta = Column(Float, nullable=False)
    fecha = Column(Date, default=datetime.date.today)
    vendedor_id = Column(Integer, ForeignKey("Usuarios.usuario_id"))

    producto = relationship("Producto", back_populates="salidas_inventario")
    cliente = relationship("Cliente", back_populates="salidas")
    vendedor = relationship("Usuario", back_populates="salidas")
    factura = relationship("Factura", back_populates="salidas")
    #edido = relationship("Pedido", back_populates="salidas")

class PedidosSalidasInventario(Base):
    __tablename__ = "PedidosSalidasInventario"

    salida_id = Column(Integer, primary_key=True, index=True)
    producto_id = Column(Integer, ForeignKey("Productos.producto_id"))
    cliente_id = Column(Integer, ForeignKey("Clientes.cliente_id"))
    pedido_id = Column(Integer, ForeignKey("Pedidos.pedido_id"), nullable=False)
    cantidad = Column(Integer, nullable=False)
    precio_venta = Column(Float, nullable=False)
    fecha = Column(Date, default=datetime.date.today)
    vendedor_id = Column(Integer, ForeignKey("Usuarios.usuario_id"))

    producto = relationship("Producto", back_populates="pedidossalidas")
    cliente = relationship("Cliente", back_populates="pedidossalidas")
    vendedor = relationship("Usuario", back_populates="pedidossalidas")
    pedido = relationship("Pedido", back_populates="pedidossalidas")

class Historial(Base):
    __tablename__ = "Historial"

    historial_id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("Usuarios.usuario_id"), nullable=False)
    accion = Column(String, nullable=False)
    fecha = Column(Date, default=datetime.date.today)
    detalles = Column(String, nullable=True)

    usuario = relationship("Usuario", back_populates="historial")
    
    
    


