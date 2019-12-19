from pymodm import MongoModel, EmbeddedMongoModel, ReferenceField, fields, connect
from models.producto import (
    SubCategoria,
    Categoria,
    Proveedor,
    AtributoDict,
    AtributoDictList,
    AtributoMagnitudDict,
    Atributos,
    Producto,
)
#from schemas.empleado import Usuario
# Establish a connection to the database.
connect('mongodb://localhost:27017/ej1')

class TarjetaPuntosModel(MongoModel):
    codigo_qr = fields.CharField()
    codigo_barras = fields.CharField()
    qr_imagen = fields.URLField()
    balance = fields.FloatField()
    fecha_creacion = fields.DateTimeField()
    fecha_vigencia = fields.DateTimeField()

##NOTE: fecha_inicio es diferente que 
##      fecha vigencia, la tarjeta de sellos
##      es por temporada, ej-. Mes Diciembre

class TarjetaSellosModel(MongoModel):
    fecha_inicio = fields.DateTimeField()
    fecha_fin = fields.DateTimeField()
    num_sellos = fields.IntegerField()
    titulo = fields.CharField()
    descripcion = fields.CharField()
    icono_off = fields.URLField()
    icono_on = fields.URLField()
    producto = fields.ReferenceField(Producto)


class HistorialTarjetaSellos(MongoModel):
    fecha_obtencion = fields.DateTimeField()
    id_tarjeta = ReferenceField(TarjetaSellosModel)
    #id_empleado_otorga = ReferenceField(Usuario)
