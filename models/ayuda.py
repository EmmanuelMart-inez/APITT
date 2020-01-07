from pymodm import connect, fields, MongoModel, EmbeddedMongoModel
# Establish a connection to the database.
connect('mongodb://localhost:27017/ej1')


class AyudaModel(MongoModel):
    imagen_icon = fields.URLField()
    titulo = fields.CharField()
    descripcion = fields.CharField()
