from ma import ma
from marshmallow import Schema, fields, ValidationError

class NotificacionSchema(ma.Schema):
    id_participante = fields.Str()
    titulo = fields.Str()
    mensaje = fields.Str()
    fecha = fields.DateTime()
    imagenIcon = fields.Str()
    bar_text = fields.Str()
    tipo_notificacion = fields.Str()
    #link_encuesta = fields.Nested(EncuestaSchema)
    #link_premio = fields.EmbeddedDocumentListField(
    #    Premio, default=[])
    #link_promocion = fields.EmbeddedDocumentListField(
    #    Promocion, default=[])

    class Meta:
        fields = (
            "id_participante",
            "titulo"
        )
