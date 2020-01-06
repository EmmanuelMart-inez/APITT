from ma import ma
from marshmallow import Schema, fields, ValidationError
# from schemas.notificacion import NotificacionSchema

class CatalogoSchema(ma.Schema):
    _id = fields.Str()
    tipo = fields.Str()
    imagen = fields.URL()
    titulo = fields.Str()
    descripcion = fields.Str()
    fecha_vigencia = fields.DateTime()
    #id_producto = fields.ReferenceField(Producto)

    class Meta:
       fields = (
            "_id", 
            "tipo", 
            "imagen", 
            "titulo", 
            "descripcion", 
            "fecha_vigencia",
            )
