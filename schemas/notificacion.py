from ma import ma
from marshmallow import Schema, fields, ValidationError

class NotificacionTemplateSchema(ma.Schema):
    _id = fields.Str()
    titulo = fields.Str()
    mensaje = fields.Str()
    fecha = fields.DateTime()
    imagenicon = fields.URL()
    bar_text = fields.Str()
    tipo_notificacion = fields.Str()
    link = fields.Str()
    filtros = fields.List(fields.Str())
    # tags = fields.List(fields.Str())

    class Meta:
        fields = (
            "_id",
            "titulo",
            "mensaje",
            "fecha",
            "imagenIcon",
            "bar_text",
            "tipo_notificacion",
            "link",
            "filtros"
        )


class NotificacionSchema(ma.Schema):
    _id = fields.Str()
    id_notificacion = fields.Str()
    id_participante = fields.Str()
    estado = fields.Integer()
    #link_encuesta = fields.Nested(EncuestaSchema)
    #link_premio = fields.EmbeddedDocumentListField(
    #    Premio, default=[])
    #link_promocion = fields.EmbeddedDocumentListField(
    #    Promocion, default=[])

    class Meta:
        fields = (
            "_id",
            "id_notificacion",
            "id_participante",
            "estado"
        )

class NotificacionSchemaExtended(ma.Schema):
    _id = fields.Str()
    id_notificacion = fields.Nested(NotificacionTemplateSchema())
    id_participante = fields.Str()
    estado = fields.Integer()
    #link_encuesta = fields.Nested(EncuestaSchema)
    #link_premio = fields.EmbeddedDocumentListField(
    #    Premio, default=[])
    #link_promocion = fields.EmbeddedDocumentListField(
    #    Promocion, default=[])

    class Meta:
        fields = (
            "_id",
            "id_notificacion",
            "id_participante",
            "estado"
        )
        exclude = ["id_notificacion.filtros", "id_participante", "estado"]
