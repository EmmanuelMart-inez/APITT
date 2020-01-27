from pymodm import connect, fields, MongoModel, EmbeddedMongoModel
from models.participante import ParticipanteModel
#from encuesta import Encuesta
#from premio import Premio
#from promocion import Promocion
# Establish a connection to the database.
connect('mongodb://localhost:27017/ej1')


class NotificacionModel(MongoModel):
    id_participante = fields.ReferenceField(ParticipanteModel)
    titulo = fields.CharField()
    mensaje = fields.CharField()
    fecha = fields.DateTimeField()
    imagenIcon = fields.URLField()
    bar_text = fields.CharField()
    tipo_notificacion = fields.CharField()
    link = fields.CharField(default="null")
    estado = fields.IntegerField()
    #link_encuesta = fields.EmbeddedDocumentListField(
    #    Encuesta, default=[])
    #link_premio = fields.EmbeddedDocumentListField(
    #    Premio, default=[])
    #link_promocion = fields.EmbeddedDocumentListField(
    #    Promocion, default=[])

class NotificacionesModel(MongoModel):
    nottts = fields.EmbeddedDocumentListField(
        NotificacionModel, default=[])