from ma import ma
from marshmallow import Schema, fields, ValidationError

class TarjetaPuntosSchema(ma.Schema):
    _id = fields.Str()
    codigo_qr = fields.Str()
    codigo_barras = fields.Str()
    qr_imagen = fields.URL()
    balance = fields.Float()
    fecha_creacion = fields.DateTime()
    fecha_vigencia = fields.DateTime()

    class Meta:
        fields = (
            "_id",
            "codigo_qr",
            "codigo_barras", 
            "qr_imagen", 
            "balance", 
            "fecha_creacion",
            "fecha_vigencia"
        )
         

class TarjetaSellosSchema(ma.Schema):
    fecha_inicio = fields.DateTime()
    fecha_fin = fields.DateTime()
    num_sellos = fields.Integer()
    titulo = fields.Str()
    descripcion = fields.Str()
    icono_off = fields.URL()
    icono_on = fields.URL()
    producto = fields.Str()

    class Meta:
        fields = (
            "fecha_inicio", 
            "fecha_fin", 
            "num_sellos", 
            "titulo", 
            "descripcion", 
            "icono_off", 
            "icono_on", 
            "producto" 
        )
