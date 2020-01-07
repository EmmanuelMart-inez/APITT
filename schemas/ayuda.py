from ma import ma
from marshmallow import Schema, fields, ValidationError

class  AyudaSchema(ma.Schema):
    _id = fields.Str()
    imagen_icon = fields.URL()
    titulo = fields.Str()
    descripcion = fields.Str()

    class Meta:
        fields = (
            "_id",
            "imagen_icon",
            "titulo",
            "descripcion",
        )