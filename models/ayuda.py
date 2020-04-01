from pymodm import connect, fields, MongoModel, EmbeddedMongoModel
from bson.objectid import ObjectId
# Establish a connection to the database.
connect('mongodb://localhost:27017/ej1')


class AyudaModel(MongoModel):
    imagen_icon = fields.URLField()
    titulo = fields.CharField()
    descripcion = fields.CharField()

    @classmethod
    def find_by_id(cls, _Objectid: str) -> "AyudaModel":
        try:
            oid = ObjectId(_Objectid)
            notif = cls.objects.get({'_id': oid})
            return notif
        except cls.DoesNotExist:
            return None

