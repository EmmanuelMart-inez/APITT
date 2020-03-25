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
    nombre = fields.CharField()
    puntos = fields.IntegerField()
    codigo_barras = fields.BigIntegerField()
    codigo_qr = fields.CharField()
    imagen_icon = fields.URLField()
    imagen_display = fields.URLField()
    fecha_creacion = fields.DateTimeField()
    fecha_vigencia = fields.DateTimeField()
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
                id_premio = p._id,
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
    id_promocion = fields.CharField() # Valor tomado del punto de venta para obtener la relación de promociones
    id_participante = fields.CharField()
    id_premio = fields.CharField()
    estado = fields.IntegerField()
    fecha_creacion = fields.DateTimeField()
    fechas_redencion = fields.ListField(fields.DateTimeField(), default=[], required=False, blank=True)

    @classmethod
    def find_by_id(cls, _Objectid: str) -> "PremioParticipanteModel":
        try:
            oid = ObjectId(_Objectid)
            notif = cls.objects.get({'_id': oid})
            print(notif)
            return notif
        except cls.DoesNotExist:
            return None 