from ma import ma
from marshmallow import Schema, fields, ValidationError

class FacebookFieldsSchema(ma.Schema):
    #public_fields = fields.CharField()
    facebook_id = fields.Str()
    name = fields.Str()
    last_name = fields.Str()
    email = fields.Email()
    birthday = fields.DateTime()
    user_photo = fields.URL()  # "Change to ImageField"
    gender = fields.Str()

    class Meta:
        fields = (
            "facebook_id", 
            "name", 
            "last_name", 
            "email", 
            "birthday",
            "user_photo",  
            "gender" 
        )

class GoogleFieldsSchema(ma.Schema):
    google_id = fields.Str()
    name = fields.Str()
    given_name = fields.Str()
    family_name = fields.Str()
    picture = fields.URL()
    email = fields.Email()
    email_verified = fields.Boolean()

    class Meta:
        fields = (
            "google_id", 
            "name", 
            "given_name", 
            "family_name", 
            "picture", 
            "email", 
            "email_verified" 
        )

class TarjetaSellosSchema(ma.Schema):
    _id = fields.Str()
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
            "_id",
            "fecha_inicio",
            "fecha_fin",
            "num_sellos", 
            "titulo", 
            "descripcion", 
            "icono_off", 
            "icono_on", 
            "producto" 
        )

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
            "_id"
            "codigo_qr",
            "codigo_barras",
            "qr_imagen", 
            "balance",
            "fecha_creacion",
            "fecha_vigencia"    
        )

class ParticipanteSchema(ma.Schema):
    _id = fields.Str()
    nombre = fields.Str()
    sexo = fields.Str(allow_none=True)
    paterno = fields.Str()
    password = fields.Str()
    email = fields.Email()
    fecha_nacimiento = fields.DateTime()
    fecha_antiguedad = fields.DateTime()
    foto = fields.URL()
    direccion =  fields.Str()
    intentos = fields.Integer()
    ultimo_inicio_sesion = fields.DateTime()
    secret_key = fields.Str()
    token_user = fields.Str()
    fresh_token = fields.Str()
    facebook_fields = fields.Nested(FacebookFieldsSchema)
    google_fields = fields.Nested(GoogleFieldsSchema)
    tarjeta_sellos = fields.Nested(TarjetaSellosSchema)
    tarjeta_puntos = fields.Nested(TarjetaPuntosSchema)

    class Meta:
        fields = (
            "_id", 
            "nombre",
            "sexo",
            "paterno",
            "password", 
            "fecha", 
            "email", 
            "fecha_nacimiento", 
            "fecha_antiguedad",
            "foto",
            "direccion",
            "intentos",
            "ultimo_inicio_sesion",
            "secret_key",
            "token_user",
            "fresh_token",
            "facebook_fields",
            "google_fields",
            "tarjeta_sellos",
            "tarjeta_puntos"
        )


"""
user = Usuario(username="Monty", db)
blog = Blog(title="Something Completely Different", author=user)
result = BlogSchema().dump(blog)
pprint(result)
"""
