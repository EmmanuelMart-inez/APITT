from pymodm import MongoModel, EmbeddedMongoModel, ReferenceField, fields, connect
from pymodm.errors import ValidationError
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
import math
from bson.objectid import ObjectId

import datetime as dt
from dateutil.relativedelta import *
import calendar
import dateutil.parser

#from schemas.empleado import Usuario
# Establish a connection to the database.
connect('mongodb://localhost:27017/ej1')

# No se usa! 
class TarjetaPuntosModel(MongoModel):
    codigo_qr = fields.CharField()
    codigo_barras = fields.CharField()
    qr_imagen = fields.CharField()
    balance = fields.FloatField()
    fecha_creacion = fields.DateTimeField()
    fecha_vigencia = fields.DateTimeField()

    @classmethod
    def find_by_id(cls, _Objectid: str) -> "TarjetaPuntosTemplateModel":
        try:
            oid = ObjectId(_Objectid)
            notif = cls.objects.get({'_id': oid})
            return notif
        except cls.DoesNotExist:
            return None

# Sistema de niveles
class TarjetaPuntosTemplateModel(MongoModel):
    titulo = fields.CharField()
    num_puntos = fields.FloatField()
    fecha_creacion = fields.DateTimeField()
    dias_vigencia = fields.IntegerField() # REMOVED: Cambiado por fecha_vencimiento TODO: Más adelante sería bueno tener esta funcionalidad
    fecha_vencimiento = fields.DateTimeField() 
    max_canjeos = fields.IntegerField() #"OBSOLET; REMOVED": se excluye desde el schema 
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
        all_levels = cls.objects.raw({'fecha_vencimiento': { "$gt" : dt.datetime.now() }})
        # all_levels = cls.objects.all()
        all_levels_ordered_by_hightest = all_levels.order_by([("num_puntos", pymongo.DESCENDING)])
        level_count = []
        current_date = dt.datetime.now()
        for level in all_levels_ordered_by_hightest:
            if level.num_puntos <= participante_puntos:
                # # Regresar solo vigentes, si no hay fecha_vencimiento, considerar vigente el nivel
                # if level.fecha_vencimiento and level.fecha_vencimiento != "null": 
                #     if current_date < level.fecha_vencimiento:
                #         level_count.append(str(level._id))
                # else:
                #     level_count.append(str(level._id))
                level_count.append(str(level._id))
        return level_count

    """
    Metodo del participante para la sección premios del app
        Regresa la lista de ids de niveles vigentes con los que cuenta
        un participante
    """
    @classmethod
    def get_level_vigentes(cls, participante_puntos: float) -> "list":
        all_levels = cls.objects.raw({'fecha_vencimiento':{ '$gt': dt.datetime.now() }})
        if not all_levels:
            return None
        all_levels_ordered_by_hightest = all_levels.order_by([("num_puntos", pymongo.DESCENDING)])
        level_count = []
        current_date = dt.datetime.now()
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
    icono_off = fields.CharField()
    icono_on = fields.CharField()
    id_notificacion = fields.CharField()
    id_promocion = fields.CharField()
    trigger = fields.CharField() # Forma de obtener un sello
    producto = fields.ListField(fields.CharField(), required=False, blank=True)
    cantidad_trigger = fields.FloatField(blank=True)

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
        al realizar una compra si el trigger de sellos es cantidad,
        tomando el listado de productos comprados y comparandolos con los productos
        que otorgan sello al ser comprados, creados por el adminstrador del sistema.
        mútiplicado por la cantidad de productos
    """
    @classmethod
    def calcular_sellos_por_productos(cls, detalle_venta: list) -> "TarjetaSellosModel":
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
        print("ticket:", list(set(prodList)))
        print("config:", list(set(last_config.producto)))
        print(sellos_products_match)
        # Multiplicar la cantidad de productos vendidos por producto
        count_sellos = 0
        for producto_comprado_con_sello in sellos_products_match:
            for producto_comprado in detalle_venta:
                if producto_comprado_con_sello == str(producto_comprado.producto._id): 
                    print("compradoda sello: {}, producto.prod._id: {}".format(producto_comprado_con_sello, str(producto_comprado.producto._id)))
                    # TODO: En un futuro se podría desear que no se de sellos si se aplicó una
                    # promocion, descuento o en realidad no se está pagando por el producto.
                    count_sellos += producto_comprado.cantidad
        # print(len(sellos_products_match))
        # print(prodList)
        return count_sellos

    """
    Calcula la cantidad de sellos obtenidos en la modalidad de cantidad gastada 
    en el total del ticket (se considera como total al total despues de impuestos y descuentos).
    """
    @classmethod 
    def calcular_sellos_por_cantidad(cls, ticket_venta: list, cantidad: float) -> "TarjetaSellosModel":
        last_config = cls.get_tarjeta_sellos_actual()
        if not last_config:
            return None
        if not last_config.producto:
            return  0
        # redondeo hacia abajo
        count_puntos = 0
        if last_config.cantidad_trigger:
            count_puntos = math.floor(ticket_venta.total / last_config.cantidad_trigger)
        return count_puntos

    
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

    