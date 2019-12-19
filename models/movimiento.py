from pymodm import connect, fields, MongoModel, EmbeddedMongoModel
from participante import Participante
from venta import Venta
# Establish a connection to the database.
connect('mongodb://localhost:27017/ej1')


class MovimientoApp(MongoModel):
    id_participante = fields.ReferenceField(Producto)
    id_venta = fields.ReferenceField(Venta)
    nombre = fields.CharField()
    tipo = fields.CharField()
    total = fields.FloatField()
    fecha = fields.DateTimeField()
    imagen_icon = fields.URLField()
