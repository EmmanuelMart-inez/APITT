import datetime as dt
import pymongo
from pymodm import connect, fields, MongoModel, EmbeddedMongoModel
from pymodm.errors import ValidationError
#from producto import Producto
from models.participante import ParticipanteModel
from bson.objectid import ObjectId
# Establish a connection to the database.
connect('mongodb://localhost:27017/ej1')

from datetime import *
from dateutil.relativedelta import *
import calendar
import dateutil.parser

class PremioModel(MongoModel):
    # _id = fields.ObjectId()
    nombre = fields.CharField()
    puntos = fields.IntegerField()
    codigo_barras = fields.BigIntegerField()
    codigo_qr = fields.CharField()
    imagen_icon = fields.CharField()
    imagen_display = fields.CharField()
    fecha_creacion = fields.DateTimeField()
    fecha_vigencia = fields.DateTimeField()
    vidas = fields.IntegerField(blank=True, required=False, default=1)
    # TODO: Default 1 es correcto?: Por ahora hace match con el acoplamiento anterior del sistema pero, ¿hay EdgeCases?
    # fecha_redencion = fields.DateTimeField()
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

    # Filtros es una lista de ids de participantes a los cuales se les enviara la notificacion
    @classmethod
    def send_to_participantes(cls, n):
        try:
            filtersObids=[]
            if not "filtros" in n:
                return {"message": "Error: Sin destinatarios, debe haber al menos un participante a quien enviarle esta acción"}
            for fil in n.filtros:
                filtersObids.append(ObjectId(fil))
            # Enviar a todos los participantes
            for par in ParticipanteModel.objects.raw({"_id": { "$in": filtersObids}}):
                # part_id = ObjectId(id)
                notif = PremioParticipanteModel(
                id_participante=par._id,
                id_premio = n.link,
                fecha_creacion=dt.datetime.now(),
                estado=0,
                # Estado puede servir para actualizar tambien OJO! ahora esta fijo, pero podrías ser variable
                ).save()     
            return {"status": 200, 
                    "total": len(filtersObids)}
                # PYMODM no tiene soporte transaccional, en un futuro migrar a PYMONGO, que sí tiene soporte
        # return {"message": "Notificacion guardada con éxito."}
        except ValidationError as exc:
            print(exc.message)
            return {"status": 404}

class PremioParticipanteModel(MongoModel):
    # _id = fields.ObjectId()
    id_promocion = fields.CharField() # Valor tomado del punto de venta para obtener la relación de promociones ##ESTE VA EN EL MODELO SUPERIOR
    id_participante = fields.CharField()
    id_premio = fields.CharField()
    estado = fields.IntegerField()
    fecha_creacion = fields.DateTimeField()
    fechas_redencion = fields.ListField(fields.DateTimeField(), default=[], required=False, blank=True)
    fecha_vencimiento = fields.DateTimeField(required=False, blank=True)
    # fechas_redencion = fields.ListField(fields.DateTimeField(), default=[], required=False, blank=True)

    @classmethod
    def find_by_id(cls, _Objectid: str) -> "PremioParticipanteModel":
        try:
            oid = ObjectId(_Objectid)
            notif = cls.objects.get({'_id': oid})
            print(notif)
            return notif
        except cls.DoesNotExist:
            return None 
    
    @classmethod
    def find_by_field(cls, field: str, value: str) -> "PremioParticipanteModel":
        try:
            premios = cls.objects.raw({field: value, })
        except cls.DoesNotExist:
            return None 
        return premios

    @classmethod 
    def find_by_two_fields(cls, field1: str, value1: str, field2: str, value2) -> "PremioParticipanteModel":
        try:
            ppremio = cls.objects.raw({field1: value1, field2: value2})
            # Match just one record
            ppremio_ordered_by_latest = ppremio.order_by([("fecha_creacion", pymongo.DESCENDING)])
            last_ppremio = ppremio_ordered_by_latest.first()
            return last_ppremio
        except cls.DoesNotExist:
            return None
    
    # Obtiene los premios validos del partipantes
    @classmethod
    def find_by_id_vigentes(cls, _Objectid: str, field: str) -> "PremioParticipanteModel":
        date_s = dt.datetime.now()
        # date_s = dateutil.parser.parse(dt.datetime.now())
        # print(type(date_s))
        # date_s = dt.datetime.fromisoformat(date_start)
        try: 
            oid = ObjectId(_Objectid)
            premios = cls.objects.raw({'id_participante' : oid, field : { "$lt": date_s}})
            return premios
        except cls.DoesNotExist:
            return None

    # """
    # Obtiene la consulta del campo y valor solicitado y de todos los resultados, toma el más
    # antiguo, no importa devolver solo uno para el caso de premios ya que las acciones
    # que se toman aplican para cualquier premio, ejemplo: eliminar un premio de X premios
    # que tienen el mismo beneficio, se toma el más antiguo para beneficiar al participante
    # con la vigencia """
    # @classmethod 
    # def find_oldest_by_field(cls, field1: str, value1) -> "PremioModel":
    #     try:
    #         premio = cls.objects.raw({field1: value1})
    #         # Match just one record OLDEST
    #         premio_ordered_by_latest = premio.order_by([("fecha_creacion", pymongo.ASCENDING)])
    #         last_premio = premio_ordered_by_latest.first()
    #         return last_premio
    #     except cls.DoesNotExist:
    #         return None
    
    # @classmethod 
    # def find_oldest_by_two_fields(cls, field1: str, value1: str, field2: str, value2: str) -> "ParticipantesEncuestaModel":
    #     try:
    #         ppremio = cls.objects.raw({field1: value1, field2: value2})
    #         # Match just one record OLDEST
    #         ppremio_ordered_by_latest = ppremio.order_by([("fecha_creacion", pymongo.ASCENDING)])
    #         last_ppremio = ppremio_ordered_by_latest.first()
    #         return last_ppremio
    #     except cls.DoesNotExist:
    #         return None