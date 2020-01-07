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
    fecha_redencion = fields.DateTime()
    #id_producto = fields.ReferenceField(default=None)
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
            "fecha_redencion",
            "id_producto",
            "id_participante"
        )