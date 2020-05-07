from pymodm import connect, fields, MongoModel, EmbeddedMongoModel
# from participante import Participante
# Establish a connection to the database.
connect('mongodb://localhost:27017/ej1')


class PromocionModel(MongoModel):
    # nombre = fields.CharField()
    titulo = fields.CharField()
    tipo = fields.CharField()
    valor = fields.FloatField()
    productos_validos = fields.ListField(fields.CharField(), default=[])
    puntos = fields.FloatField()
    sellos = fields.IntegerField()
    descripcion = fields.CharField()
    descuento_porciento = fields.FloatField()
    descuento_pesos = fields.FloatField()
    descuento_producto = fields.FloatField()
    descuento_categoria = fields.CharField()
    fecha_creacion = fields.DateTimeField()
    fecha_vigencia = fields.DateTimeField()
    fecha_redencion = fields.DateTimeField()
    imagen_miniatura = fields.CharField()
    imagen_display = fields.CharField()
    codigo_barras = fields.CharField()
    codigo_qr = fields.CharField()
    # id_participante = fields.ReferenceField(Participante)
