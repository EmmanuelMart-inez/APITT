from pymodm import connect, fields, MongoModel, EmbeddedMongoModel
from participante import Participante
from producto import Producto
from empleado import Usuario


class FormaPago(EmbeddedMongoModel):
    nombre = fields.CharField()
    otros_detalles = fields.CharField()
    estado = fields.CharField()
    total = fields.FloatField()


class detalleVenta(EmbeddedMongoModel):
    cantidad = fields.IntegerField()
    precio = fields.FloatField()
    impuestos = fields.FloatField()
    descuento_producto = fields.IntegerField()
    importe = fields.IntegerField()
    producto = fields.EmbeddedDocumentField(
        Producto)


class Venta(MongoModel):
    total = fields.FloatField()
    fecha = fields.DateTimeField()
    descuento_general = fields.FloatField()
    codigo_qr = fields.CharField()
    forma_pago = fields.EmbeddedDocumentField(
        FormaPago)
    detalle_venta = fields.EmbeddedDocumentListField(
        FacebookFields, default=[])
    id_vendedor = fields.ReferenceField(Usuario)
    id_participante = fields.ReferenceField(Participante)
