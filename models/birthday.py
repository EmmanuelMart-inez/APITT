from pymodm import connect, fields, MongoModel, EmbeddedMongoModel
from models.promocion import PromocionModel
from models.notificacion import NotificacionModel
# Establish a connection to the database.
connect('mongodb://localhost:27017/ej1')
from pymodm import connect, fields, MongoModel, EmbeddedMongoModel
from pymodm.errors import ValidationError

from bson.objectid import ObjectId
# Establish a connection to the database.
connect('mongodb://localhost:27017/ej1')



class BirthdayModel(MongoModel):
    # tipo = fields.CharField()
    id_notificacion = fields.CharField()
    id_promocion = fields.CharField()   
    # id_notificacion = fields.EmbeddedDocumentListField(NotificacionModel)
    # id_promocion = fields.EmbeddedDocumentListField(PromocionModel)   
    antiguedad = fields.IntegerField()
    trigger = fields.IntegerField()
    vigencia = fields.CharField()
    # Antiguedad_necesaria = fields.IntegerField() Días de antiguedad
    fecha_creacion = fields.DateTimeField()

    @classmethod
    def find_by_id(cls, _Objectid: str) -> "BirthdayModel":
        try:
            oid = ObjectId(_Objectid)
            notif = cls.objects.get({'_id': oid})
            print(notif)
            return notif
        except cls.DoesNotExist:
            return None
