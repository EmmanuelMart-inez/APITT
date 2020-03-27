from ma import ma
from marshmallow import Schema, fields, ValidationError

class PromocionSchema(ma.Schema):
    _id = fields.Str()
    titulo = fields.Str()
    descripcion = fields.Str()
    imagen = fields.URL()
    precio_venta = fields.Float()
    costo_venta = fields.Float()
    fecha_vigencia_start = fields.DateTime()
    fecha_vigencia_end = fields.DateTime()

    class Meta:
        fields = (
            "_id",
            "titulo",
            "descripcion",
            "imagen",
            "precio_venta",
            "costo_venta",
            "fecha_vigencia_start",
            "fecha_vigencia_end",
        ) 