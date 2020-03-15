from pymodm import connect, fields, MongoModel, EmbeddedMongoModel
#from producto import Producto
from models.participante import ParticipanteModel
from bson.objectid import ObjectId
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
    # id_participante = fields.ReferenceField(ParticipanteModel) Quita al poner la segmentación: "ninguna"

    @classmethod
    def find_by_id(cls, _Objectid: str) -> "PremioModel":
        try:
            oid = ObjectId(_Objectid)
            notif = cls.objects.get({'_id': oid})
            print(notif)
            return notif
        except cls.DoesNotExist:
            return None

class PremioParticipanteModel(MongoModel):
    id_promocion = fields.CharField() 
    id_participante = fields.ReferenceField(ParticipanteModel)
    id_premio = fields.ReferenceField(PremioModel)
    estado = fields.IntegerField()
    fechas_redencion = fields.ListField(fields.DateTimeField(), default=[], required=False, blank=True)
    # id_promocion = fields.CharField() # Valor tomado del punto de venta para obtener la relación de promociones 