from pymodm import connect, fields, MongoModel, EmbeddedMongoModel
from models.participante import ParticipanteModel
# from venta import Venta
# Establish a connection to the database.
connect('mongodb://localhost:27017/ej1')


class MovimientoAppModel(MongoModel):
    id_participante = fields.ReferenceField(ParticipanteModel)
    # id_venta = fields.ReferenceField(Venta)
    nombre = fields.CharField()
    tipo = fields.CharField()
    total = fields.FloatField()
    fecha = fields.DateTimeField()
    imagen_icon = fields.URLField()
