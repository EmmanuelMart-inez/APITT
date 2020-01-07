from pymodm import connect, fields, MongoModel, EmbeddedMongoModel
#from producto import Producto
from models.participante import ParticipanteModel
# Establish a connection to the database.
connect('mongodb://localhost:27017/ej1')


class PremioModel(MongoModel):
    nombre = fields.CharField()
    puntos = fields.IntegerField()
    codigo_barras = fields.BigIntegerField()
    codigo_qr = fields.CharField()
    imagen_icon = fields.URLField()
    imagen_display = fields.URLField()
    fecha_creacion = fields.DateTimeField()
    fecha_vigencia = fields.DateTimeField()
    fecha_redencion = fields.DateTimeField()
    #id_producto = fields.ReferenceField(Producto)
    id_participante = fields.ReferenceField(ParticipanteModel)
