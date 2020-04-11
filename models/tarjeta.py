from pymodm import MongoModel, EmbeddedMongoModel, ReferenceField, fields, connect
from models.producto import (
    SubCategoriaModel,
    CategoriaModel,
    ProveedorModel,
    AtributoDict,
    AtributoDictList,
    AtributoMagnitudDict,
    Atributos,
    ProductoModel,
)
from bson.objectid import ObjectId

from datetime import *
from dateutil.relativedelta import *
import calendar
import dateutil.parser

#from schemas.empleado import Usuario
# Establish a connection to the database.
connect('mongodb://localhost:27017/ej1')

class TarjetaPuntosModel(MongoModel):
    codigo_qr = fields.CharField()
    codigo_barras = fields.CharField()
    qr_imagen = fields.URLField()
    balance = fields.FloatField()
    fecha_creacion = fields.DateTimeField()
    fecha_vigencia = fields.DateTimeField()


class TarjetaPuntosTemplateModel(MongoModel):
    num_puntos = fields.FloatField()
    fecha_creacion = fields.DateTimeField()
    dias_vigencia = fields.IntegerField()
    # fecha_vigencia = fields.DateTimeField()
    # fecha_inicio = fields.DateTimeField()
    # fecha_fin = fields.DateTimeField()
    id_notificacion = fields.CharField()
    id_promocion = fields.CharField()
    
    @classmethod
    def find_by_id(cls, _Objectid: str) -> "AyudaModel":
        try:
            oid = ObjectId(_Objectid)
            notif = cls.objects.get({'_id': oid})
            return notif
        except cls.DoesNotExist:
            return None

##NOTE: fecha_inicio es diferente que 
##      fecha vigencia, la tarjeta de sellos
##      es por temporada, ej-. Mes Diciembre

class TarjetaSellosModel(MongoModel):
    fecha_creacion = fields.DateTimeField()
    fecha_inicio = fields.DateTimeField()
    fecha_fin = fields.DateTimeField()
    num_sellos = fields.IntegerField()
    titulo = fields.CharField()
    descripcion = fields.CharField()
    icono_off = fields.URLField()
    icono_on = fields.URLField()
    producto = fields.ListField(fields.CharField())
    cantidad_trigger = fields.FloatField()

    @classmethod
    def find_by_id(cls, _Objectid: str) -> "AyudaModel":
        try:
            oid = ObjectId(_Objectid)
            notif = cls.objects.get({'_id': oid})
            return notif
        except cls.DoesNotExist:
            return None
    
class HistorialTarjetaSellos(MongoModel):
    fecha_obtencion = fields.DateTimeField()
    id_tarjeta = fields.CharField()
    total_sellos = fields.CharField()
    # id_tarjeta = ReferenceField(TarjetaSellosModel)
    # total_sellos = fields.IntegerField()
    #id_empleado_otorga = ReferenceField(Usuario)

    