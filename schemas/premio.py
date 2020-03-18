from ma import ma
from marshmallow import Schema, fields, ValidationError
from schemas.notificacion import NotificacionSchema


class PremioSchema(ma.Schema):
    _id = fields.Str()
    nombre = fields.Str()
    puntos = fields.Integer()
    codigo_barras = fields.Integer()
    codigo_qr = fields.Str()
    imagen_icon = fields.URL()
    imagen_display = fields.URL()
    fecha_creacion = fields.DateTime()
    fecha_vigencia = fields.DateTime()
    #  = fields.ReferenceField(default=None)
    id_participante = fields.Str()

    class Meta:
        fields = (
            "_id",
            "nombre", 
            "puntos", 
            "codigo_barras", 
            "codigo_qr",
            "imagen_icon",
            "imagen_display",
            "fecha_creacion", 
            "fecha_vigencia", 
            "id_producto",
            "id_participante"
        )

class PremioParticipanteSchema(ma.Schema):
    _id = fields.Str()
    id_participante = fields.Str()
    id_premio = fields.Str()
    id_promocion = fields.Str()
    estado = fields.Integer()
    fecha_creacion = fields.DateTime()
    fechas_redencion = fields.List(fields.DateTime)

    class Meta:
        fields = (
            "_id",
            "id_participante",
            "id_premio",
            "id_promocion",
            "estado",
            "fecha_creacion",
            "fechas_redencion"
        )