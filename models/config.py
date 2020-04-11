from pymodm import connect, fields, MongoModel, EmbeddedMongoModel
# Establish a connection to the database.
connect('mongodb://localhost:27017/ej1')
from pymodm import connect, fields, MongoModel, EmbeddedMongoModel
from pymodm.errors import ValidationError

from bson.objectid import ObjectId
# Establish a connection to the database.
connect('mongodb://localhost:27017/ej1')

# Constants and config model for global preferences and modules
# activated on the loyalty program
class ConfigModel(MongoModel):
    fecha_creacion = fields.DateTimeField()
    equivalencia_punto_pesos = fields.FloatField()
    
    @classmethod
    def find_by_id(cls, _Objectid: str) -> "AyudaModel":
        try:
            oid = ObjectId(_Objectid)
            notif = cls.objects.get({'_id': oid})
            return notif
        except cls.DoesNotExist:
            return None