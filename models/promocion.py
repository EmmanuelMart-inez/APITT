from pymodm import connect, fields, MongoModel, EmbeddedMongoModel
from participante import Participante
# Establish a connection to the database.
connect('mongodb://localhost:27017/ej1')


class Promocion(MongoModel):
    nombre = fields.CharField()
    descripcion = fields.CharField()
    descuento_porciento = fields.FloatField()
    descuento_pesos = fields.FloatField()
    descuento_producto = fields.FloatField()
    descuento_categoria = fields.CharField()
    fecha_creacion = fields.DateTimeField()
    fecha_vigencia = fields.DateTimeField()
    fecha_redencion = fields.DateTimeField()
    imagen_miniatura = fields.URLField()
    imagen_display = fields.URLField()
    codigo_barras = fields.CharField()
    codigo_qr = fields.CharField()
    id_participante = fields.ReferenceField(Participante)
