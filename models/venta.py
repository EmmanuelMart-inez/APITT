from pymodm import connect, fields, MongoModel, EmbeddedMongoModel
import pymongo
# from participante import Participante
from models.producto import ProductoModel
from models.empleado import UsuarioModel

from datetime import *
from dateutil.relativedelta import *
import calendar
import dateutil.parser

class FormaPagoModel(EmbeddedMongoModel):
    nombre = fields.CharField()
    otros_detalles = fields.CharField()
    estado = fields.CharField()
    total = fields.FloatField()


class detalleVentaModel(EmbeddedMongoModel):
    cantidad = fields.IntegerField()
    precio = fields.FloatField()
    # impuestos = fields.FloatField()
    descuento_producto = fields.IntegerField()
    importe = fields.IntegerField()
    producto = fields.EmbeddedDocumentField(
        ProductoModel)


class VentaModel(MongoModel):
    total = fields.FloatField()
    descuento = fields.FloatField()
    promociones = fields.ListField(fields.CharField(), default=[], blank=True)
    # subtotal = fields.FloatField
    # impuestos = fields.FloatField()
    # cambio = fields.FloatField()
    fecha = fields.DateTimeField()
    descuento_general = fields.FloatField()
    codigo_qr = fields.CharField()
    forma_pago = fields.EmbeddedDocumentField(
        FormaPagoModel)
    detalle_venta = fields.EmbeddedDocumentListField(
        detalleVentaModel, default=[])
    id_vendedor = fields.CharField()
    id_participante = fields.CharField()
    id_ticket_punto_venta = fields.CharField()
    estado = fields.CharField(blank=True, required=False)
    # Transacción ==> id_movimiento Movimiento(nested(Venta, Notificacion(nested(Premio, encuesta)), Nivel(nested(Notificacion(nested(Premio, encuesta)))), Promocion?)
    puntos_otorgados = fields.FloatField(blank=True, required=False)
    sellos_otorgados = fields.IntegerField(blank=True, required=False)
    id_notificacion_obtenidas_list = fields.ListField(fields.CharField(), default=[])

    @classmethod
    def find_by_id(cls, _Objectid: str, isString: bool) -> "VentaModel":
        try:
            oid = ObjectId(_Objectid)
            notif = cls.objects.get({'_id': oid})
            return notif
        except cls.DoesNotExist:
            return None
        except cls.MultipleObjectsReturned:
            return None

    @classmethod
    def find_by_field(cls, field: str, value: str) -> "VentaModel":
        try:
            notif = cls.objects.get({ field: value })
            return notif
        except cls.DoesNotExist:
            return None

    @classmethod
    def filter_by_date_range(cls, date_start: str, date_end: str, field: str) -> "ParticipanteModel":
        date_s = dateutil.parser.parse(date_start)
        date_e = dateutil.parser.parse(date_end)
        # print(type(date_s))
        # date_s = dt.datetime.fromisoformat(date_start)
        try: 
            users = cls.objects.raw({field : {"$gte" : date_s, "$lt": date_e}}) 
            # users = list(cls.objects.raw({'fecha_antiguedad' : date_s}) )
            # print(users)
            print(list(users))
            return users
        except cls.DoesNotExist:
            return None
            
    @classmethod
    def filter_by_date(cls, date_start: str, tipo: str, scale: str, scale_value: int, field: str) -> "ParticipanteModel":
        date_s = dateutil.parser.parse(date_start)
        # print(type(date_s))
        # date_s = dt.datetime.fromisoformat(date_start)
        try: 
            # Relative Dates
            if tipo == 'anterior':
                if scale == 'dias':
                    rdate = date_s.replace(hour=0, minute=0, second=0, microsecond=0)-relativedelta(days=+scale_value)
                elif scale == 'semanas':
                    rdate = date_s.replace(hour=0, minute=0, second=0, microsecond=0)-relativedelta(weeks=+scale_value)
                elif scale == 'meses':
                    rdate = date_s.replace(hour=0, minute=0, second=0, microsecond=0)-relativedelta(months=+scale_value)
                elif scale == 'años':
                    rdate = date_s.replace(hour=0, minute=0, second=0, microsecond=0)-relativedelta(years=+scale_value)
                elif scale == 'minutos':
                    rdate = date_s-relativedelta(minutes=+scale_value)
                elif scale == 'horas':
                    rdate = date_s-relativedelta(hours=+scale_value)
                users = cls.objects.raw({field : {"$gte" : rdate, "$lt": date_s}})
                return users
            elif tipo == 'siguiente':
                if scale == 'dias':
                    rdate = date_s.replace(hour=23, minute=59, second=59, microsecond=59)+relativedelta(days=+scale_value)
                elif scale == 'semanas':
                    rdate = date_s.replace(hour=23, minute=59, second=59, microsecond=59)+relativedelta(weeks=+scale_value)
                elif scale == 'meses':
                    rdate = date_s.replace(hour=23, minute=59, second=59, microsecond=59)+relativedelta(months=+scale_value)
                elif scale == 'años':
                    rdate = date_s.replace(hour=23, minute=59, second=59, microsecond=59)+relativedelta(years=+scale_value)
                elif scale == 'minutos':
                    rdate = date_s+relativedelta(minutes=+scale_value)
                elif scale == 'horas':
                    rdate = date_s+relativedelta(hours=+scale_value)
                users = cls.objects.raw({field : {"$gte" : date_s, "$lt": rdate.replace(hour=23, minute=59, second=59, microsecond=59)}})
                return users
            # NOTE: No importa el valor de `scale_value` en esta consulta
            elif tipo == 'actual':
                if scale == 'dias':
                    rdate = date_s.replace(hour=0, minute=0, second=0, microsecond=0)
                # Forma de calcular los dias a restar para obtener la semana actual = #día % 8 - 1
                elif scale == 'semanas':
                    month_day = date_s.day % 8 - 1
                    print(month_day)
                    rdate = date_s.replace(day=month_day, hour=0, minute=0, second=0, microsecond=0)+relativedelta()
                elif scale == 'meses':
                    rdate = date_s.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
                elif scale == 'años':
                    rdate = date_s.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
                elif scale == 'minutos':
                    rdate = date_s.replace(second=0, microsecond=0)
                elif scale == 'horas':
                    rdate = date_s.replace(minute=0, second=0, microsecond=0)
                else:
                    return None
                users = cls.objects.raw({field : {"$gte" : rdate, "$lt": date_s}})
                return users
            elif tipo == 'antes':
                users = cls.objects.raw({field : { "$lt": date_s}})
                return users
            elif tipo == 'despues':
                users = cls.objects.raw({field : { "$gte": date_s}})
                return users
            return {'message': 'Tipo de filtro de fecha invalido'}, 400
        except cls.DoesNotExist:
            return None

    @classmethod
    def filter_by_float_range(cls, tipo: str, field: str, float1: float, float2: float) -> "ParticipanteModel":
        if tipo == '<>':
            try:
                users = cls.objects.raw({field : { "$gte" : float1, "$lte" : float2}})
                return users
            except cls.DoesNotExist:
                return None

    @classmethod
    def filter_by_float(cls, tipo: str, float1: float, field: str) -> "ParticipanteModel":
        try:
            if tipo == '=':
                users = cls.objects.raw({field : float1})
                return users
            elif tipo == '>':
                users = cls.objects.raw({field : { "$gt" : float1}})
                return users
            elif tipo == '>=':
                users = cls.objects.raw({field : { "$gte" : float1}})
                return users
            elif tipo == '<':
                users = cls.objects.raw({field : { "$lt" : float1}})
                return users
            elif tipo == '<=':
                users = cls.objects.raw({field : { "$lte" : float1}})
                return users
            return {'message': 'Tipo de filtro de flotante invalido'}, 400
        except cls.DoesNotExist:
            return None

    @classmethod
    def filter_by_integer_range(cls, tipo: str, field: str, int1: int, int2: int) -> "ParticipanteModel":
        if tipo == '<>':
            try:
                users = cls.objects.raw({field : { "$gte" : int1, "$lte" : int2}})
                return users
            except cls.DoesNotExist:
                return None

    @classmethod
    def filter_by_integer(cls, tipo: str, int1: int, field: str) -> "ParticipanteModel":
        try:
            if tipo == '=':
                users = cls.objects.raw({field : int1})
                return users
            elif tipo == '>':
                users = cls.objects.raw({field : { "$gt" : int1}})
                return users
            elif tipo == '=>':
                users = cls.objects.raw({field : { "$gte" : int1}})
                return users
            elif tipo == '<':
                users = cls.objects.raw({field : { "$lt" : int1}})
                return users
            elif tipo == '<=':
                users = cls.objects.raw({field : { "$lte" : int1}})
                return users
            return {'message': 'Tipo de filtro de flotante invalido'}, 400
        except cls.DoesNotExist:
            return None
    
    @classmethod
    def filter_by_string(cls, field: str, tipo: str, str1: str) -> "ParticipanteModel":
        try:
            if tipo == 'es':
                users = cls.objects.raw({field : str1})
            elif tipo == 'no es':
                return users
                users = cls.objects.raw({field : { "$ne" : str2} })
            elif tipo == 'contiene':
                str2 = "/^{}$".format(str1)
                users = cls.objects.raw({field :  str2 })
                return users
            elif tipo == 'no contiene': 
                str2 = "/^{}$".format(str1)
                users = cls.objects.raw({field : { "$not" : str2}})  
                return users
            return {'message': 'Tipo de filtro de flotante invalido'}, 400     
        except cls.DoesNotExist:
            return None


