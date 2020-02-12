from pymodm import connect, fields, MongoModel, EmbeddedMongoModel
from models.participante import ParticipanteModel
from bson.objectid import ObjectId
# Establish a connection to the database.
connect('mongodb://localhost:27017/ej1')


class EncuestaOpcionesModel(MongoModel):
    descripcion = fields.CharField()
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
        EncuestaOpcionesModel, default=[])


class EncuestaModel(MongoModel):
    titulo = fields.CharField()
    categoria = fields.CharField()
    fecha_creacion = fields.DateTimeField()
    metrica = fields.CharField()
    puntos = fields.FloatField()
    paginas = fields.EmbeddedDocumentListField(
        EncuestaPaginaModel, default=[])
    
class ParticipantesEncuestaModel(MongoModel):
    id_participante = fields.ReferenceField(ParticipanteModel)
    id_encuesta = fields.ReferenceField(EncuestaModel)
    fecha_respuesta = fields.DateTimeField()
    estado = fields.CharField()
    respuestas = fields.ListField(fields.CharField(), default=[], required=False)

    @classmethod
    def find_by_id(cls, _Objectid: str) -> "ParticipantesEncuestaModel":
        try:
            oid = ObjectId(_Objectid)
            pencuesta = cls.objects.get({'_id': oid})
            return pencuesta
        except cls.DoesNotExist:
            return None