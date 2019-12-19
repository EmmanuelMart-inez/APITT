from pymodm import connect, fields, MongoModel, EmbeddedMongoModel

# Establish a connection to the database.
connect('mongodb://localhost:27017/ej1')


class EncuestaOpciones(MongoModel):
    descripcion = fields.CharField()
    calificacion = fields.CharField()
    rubrica = fields.IntegerField()


class EncuestaPagina(MongoModel):
    titulo = fields.CharField()
    tipo = fields.CharField()
    metrica = fields.CharField()
    opciones: = fields.EmbeddedDocumentListField(
        EncuestaOpciones, default=[])
    repuesta: fields.CharField()


class Encuesta(MongoModel):
    titulo = fields.CharField()
    categoria = fields.CharField()
    fecha_creacion = fields.DateTimeField()
    fecha_respuesta = fields.DateTimeField()
    metrica = fields.CharField()
    puntos = fields.IntegerField()
    paginas = fields.ReferenceField(EncuestaPagina)
    id_participante = fields.ReferenceField(Participante)
