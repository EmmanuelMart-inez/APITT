from ma import ma
from marshmallow import Schema, fields, ValidationError
from schemas.notificacion import NotificacionSchema
from schemas.promocion import PromocionSchema

class BirthdaySchema(ma.Schema):
    _id = fields.Str()
    # tipo = fields.Str()
    id_notificacion = fields.Str( required=False)
    id_promocion = fields.Str( required=False)   
    trigger = fields.Integer()
    antiguedad = fields.Integer()
    vigencia = fields.Str()
    fecha_creación = fields.DateTime()

    class Meta:
        fields = (
            "_id",
            "tipo",
            "id_notificacion",
            "id_promocion",
            "trigger",
            "antiguedad",
            "vigencia",
            "fecha_creacion"
        )
