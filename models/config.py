from pymodm import connect, fields, MongoModel, EmbeddedMongoModel
import pymongo
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
    def find_by_id(cls, _Objectid: str) -> "ConfigModel":
        try:
            oid = ObjectId(_Objectid)
            notif = cls.objects.get({'_id': oid})
            return notif
        except cls.DoesNotExist:
            return None

    """ Calcula los puntos que obtiene un cliente
        al realizar una compra por un total de X$ segun la equivalencia_punto_pesos
        dada por el administrador del sistema
    """
    @classmethod
    def calcular_puntos(cls, total_pesos: float):
        allconfig = ConfigModel.objects.all()
        allconfig_ordered_by_latest = allconfig.order_by([("fecha_creacion", pymongo.DESCENDING)])
        last_config = allconfig_ordered_by_latest.first()
        if not last_config:
            return None
        if not last_config.equivalencia_punto_pesos:
            return  0
        return total_pesos / last_config.equivalencia_punto_pesos
