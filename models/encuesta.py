from pymodm import connect, fields, MongoModel, EmbeddedMongoModel
from models.participante import ParticipanteModel
from pymodm.errors import ValidationError
from bson.objectid import ObjectId
# Establish a connection to the database.
connect('mongodb://localhost:27017/ej1')

import datetime as dt

class EncuestaOpcionesModel(MongoModel):
    # descripcion = fields.CharField(default="")
    calificacion = fields.CharField()
    rubrica = fields.FloatField()
    icon = fields.URLField()
    # Icono sirve para las encuestas del tipo
    # emogie y puede ser un gif animado

class EncuestaPaginaModel(MongoModel):
    titulo = fields.CharField()
    tipo = fields.CharField()
    metrica = fields.CharField()
    opciones = fields.EmbeddedDocumentListField(
        EncuestaOpcionesModel, blank=True)
        # EncuestaOpcionesModel, default=[])


class EncuestaModel(MongoModel):
    titulo = fields.CharField()
    categoria = fields.CharField()
    fecha_creacion = fields.DateTimeField()
    metrica = fields.CharField()
    puntos = fields.FloatField()
    paginas = fields.EmbeddedDocumentListField(
        EncuestaPaginaModel, default=[], required=False)

    @classmethod
    def find_by_id(cls, _Objectid: str) -> "EncuestaModel":
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
            for p in ParticipanteModel.objects.raw({"_id": { "$in": filtersObids}}):
                # part_id = ObjectId(id)
                notif = ParticipantesEncuestaModel(
                id_participante=p._id,
                id_encuesta=n.link,
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
   
class ParticipantesEncuestaModel(MongoModel):
    id_participante = fields.CharField()
    # id_encuesta = fields.ReferenceField(EncuestaModel)
    id_encuesta = fields.CharField()
    fecha_respuesta = fields.DateTimeField()
    estado = fields.CharField()
    fecha_creacion = fields.DateTimeField()
    respuestas = fields.ListField(fields.CharField(), default=[], required=False)
    # fecha_creacion = AFTER

    @classmethod
    def find_by_id(cls, _Objectid: str) -> "ParticipantesEncuestaModel":
        try:
            oid = ObjectId(_Objectid)
            notif = cls.objects.get({'_id': oid})
            print(notif)
            return notif
        except cls.DoesNotExist:
            return None