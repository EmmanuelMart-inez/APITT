from ma import ma
from marshmallow import Schema, fields, ValidationError
from schemas.participante import ParticipanteSchema


class EncuestaOpcionesSchema(ma.Schema):
    descripcion = fields.Str()
    calificacion = fields.Str()
    rubrica = fields.Float()
    icon = fields.URL()

    class Meta: 
        fields = (
            "descripcion",
            "calificacion",
            "rubrica",
            "icon"
        )


class EncuestaPaginaSchema(ma.Schema):
    titulo = fields.Str()
    tipo = fields.Str()
    metrica = fields.Str()
    opciones = fields.List(fields.Nested(EncuestaOpcionesSchema))

    class Meta:
        fields = (
            "titulo",
            "tipo",
            "metrica",
            "opciones",
        )


class EncuestaSchema(ma.Schema):
    _id = fields.Str()
    titulo = fields.Str()
    categoria = fields.Str()
    fecha_creacion = fields.DateTime()
    fecha_respuesta = fields.DateTime()
    metrica = fields.Str()
    estado = fields.Integer()
    puntos = fields.Float()
    paginas = fields.List(fields.Nested(EncuestaPaginaSchema))

    class Meta:
        fields = (
            "_id",
            "titulo",
            "categoria",
            "fecha_creacion",
            "fecha_respuesta",
            "metrica",
            "puntos",
            "paginas",
        )

class ParticipanteEncuestaSchema(ma.Schema):
    _id = fields.Str()
    id_participante = fields.Str()
    id_encuesta = fields.Str()
    fecha_respuesta = fields.DateTime()
    estado = fields.Str()
    respuestas = fields.List(fields.Str)

    class Meta:
        fields = (
            "_id",
            "id_participante",
            "id_encuesta",
            "fecha_respuesta",
            "estado",
            "respuestas"
        )