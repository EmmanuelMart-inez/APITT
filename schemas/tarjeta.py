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


class TarjetaPuntosTemplateSchema(ma.Schema):
    _id = fields.Str()
    titulo = fields.Str()
    num_puntos = fields.Float()
    fecha_creacion = fields.DateTime()
    dias_vigencia = fields.Integer()
    max_canjeos = fields.Integer()
    id_notificacion = fields.Str()
    id_promocion = fields.Str()

    class Meta:
        fields = (
            "_id",
            "num_puntos",
            "fecha_creacion",
            "dias_vigencia",
            "id_notificacion",
            "id_promocion"
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
            "total_sellos",
            "titulo", 
            "descripcion", 
            "icono_off", 
            "icono_on", 
            "producto"
        )


class TarjetaSellosTemplateSchema(ma.Schema):
    _id = fields.Str()
    fecha_creacion = fields.DateTime()
    fecha_inicio = fields.DateTime()
    fecha_fin = fields.DateTime()
    num_sellos = fields.Integer()
    titulo = fields.Str()
    descripcion = fields.Str()
    icono_off = fields.URL()
    icono_on = fields.URL()
    producto = fields.List(fields.Str())
    cantidad_trigger = fields.Float()

    class Meta:
        fields = (
            "_id",
            "fecha_creacion",
            "fecha_inicio", 
            "fecha_fin", 
            "num_sellos", 
            "total_sellos",
            "titulo", 
            "descripcion", 
            "icono_off", 
            "icono_on", 
            "producto",
            "cantidad_trigger"  
        )
