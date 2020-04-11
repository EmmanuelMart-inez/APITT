from ma import ma
from marshmallow import Schema, fields, ValidationError

class ConfigSchema(ma.Schema):
    _id = fields.Str()
    fecha_creacion = fields.DateTime()
    equivalencia_punto_pesos = fields.Float()

    class Meta:
        fields = (
            "_id",
            "fecha_creacion",
            "equivalencia_punto_pesos"
        )
