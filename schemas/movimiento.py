from ma import ma
from marshmallow import Schema, fields, ValidationError
from schemas.participante import ParticipanteSchema
# from schemas.venta import VentaSchema

class MovimientoAppSchema(ma.Schema): 
    _id = fields.Str()
    id_participante = fields.Str()
    nombre = fields.Str()
    tipo = fields.Str()
    total = fields.Float()
    fecha = fields.DateTime()
    imagen_icon = fields.URL()

    class Meta: 
        fields = (
            "_id",
            "id_participante",
            "nombre",
            "tipo",
            "total",
            "fecha",
            "imagen_icon"
        )


