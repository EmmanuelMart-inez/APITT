from pymodm import MongoModel, EmbeddedMongoModel, ReferenceField, fields, connect
import pymongo
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

# Sistema de niveles
class TarjetaPuntosTemplateModel(MongoModel):
    titulo = fields.CharField()
    num_puntos = fields.FloatField()
    fecha_creacion = fields.DateTimeField()
    dias_vigencia = fields.IntegerField()
    max_canjeos = fields.IntegerField()
    # fecha_vigencia = fields.DateTimeField()
    # fecha_inicio = fields.DateTimeField()
    # fecha_fin = fields.DateTimeField()
    id_notificacion = fields.CharField()
    id_promocion = fields.CharField()
    
    @classmethod
    def find_by_id(cls, _Objectid: str) -> "TarjetaPuntosTemplateModel":
        try:
            oid = ObjectId(_Objectid)
            notif = cls.objects.get({'_id': oid})
            return notif
        except cls.DoesNotExist:
            return None

    """Regresa la lista de ids de niveles con los que cuenta 
        un participante, de acuerdo a numero de puntos
        que ha obtenido
    """
    @classmethod
    def get_level(cls, participante_puntos: float) -> "list":
        all_levels = cls.objects.all()
        all_levels_ordered_by_hightest = all_levels.order_by([("num_puntos", pymongo.DESCENDING)])
        level_count = []
        for level in all_levels_ordered_by_hightest:
            if level.num_puntos <= participante_puntos:
                level_count.append(str(level._id))
        return level_count

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
    def find_by_id(cls, _Objectid: str) -> "TarjetaSellosModel":
        try:
            oid = ObjectId(_Objectid)
            notif = cls.objects.get({'_id': oid})
            return notif
        except cls.DoesNotExist:
            return None

    """
        Obtiene la configuración de la tarjeta de sellos
        más reciente.
    """
    @classmethod
    def get_tarjeta_sellos_actual(cls) -> "TarjetaSellosModel":
        allconfig = TarjetaSellosModel.objects.all()
        allconfig_ordered_by_latest = allconfig.order_by([("fecha_creacion", pymongo.DESCENDING)])
        last_config = allconfig_ordered_by_latest.first()
        return last_config

    """ Calcula los sellos que obtiene un cliente
        al realizar una compra tomando el listado de 
        productos comprados y comparandolos con los productos
        que otorgan sello al ser comprados, creados por el 
        adminstrador del sistema.
    """
    @classmethod
    def calcular_sellos(cls, detalle_venta: list) -> "TarjetaSellosModel":
        last_config = cls.get_tarjeta_sellos_actual()
        if not last_config:
            return None
        if not last_config.producto:
            return  0
        prodList = []
        for prod in detalle_venta:
            prodList.append(str(prod.producto._id))
        # Intersección de listas de productos validos vs productos en el ticket 
        sellos_products_match = list(set(prodList) & set(last_config.producto))
        # print(len(sellos_products_match))
        # print(prodList)
        return len(sellos_products_match)

    
class HistorialTarjetaSellos(MongoModel):
    fecha_obtencion = fields.DateTimeField()
    id_tarjeta = fields.CharField()
    id_participante = fields.CharField()
    total_sellos = fields.CharField()
    # id_tarjeta = ReferenceField(TarjetaSellosModel)
    # total_sellos = fields.IntegerField()
    #id_empleado_otorga = ReferenceField(Usuario)

    @classmethod
    def add_movimiento(cls, id_par, id_tarjeta) -> "NotificacionModel":
        try:
            movimiento = cls(
                id_participante=id_par,
                id_tarjeta = id_tarjeta,
                fecha_obtencion=dt.datetime.now(),
            ).save()            
        except ValidationError as exc:   
            return None
        return movimiento

    