#from schemas.user import UserSchema
from pymodm import MongoModel, EmbeddedMongoModel, ReferenceField, fields, connect


# Establish a connection to the database.
connect('mongodb://localhost:27017/ej1')
#user_schema = UserSchema()


class EmpleadoPuesto(MongoModel):
    nombre = fields.CharField()


class Empleado(MongoModel):
    nombre = fields.CharField()
    paterno = fields.CharField()
    materno = fields.CharField()
    fecha_nacimiento = fields.DateTimeField()
    fecha_contratacion = fields.DateTimeField()
    direccion = fields.CharField()
    ciudad = fields.CharField()
    codigo_postal = fields.IntegerField()
    telefono_movil = fields.BigIntegerField()
    telefono_casa = fields.BigIntegerField()
    correo = fields.EmailField()
    puesto = fields.EmbeddedDocumentField(EmpleadoPuesto)


class Cajero(MongoModel):
    alias = fields.CharField()


class Usuario(MongoModel):
    username = fields.CharField()
    password = fields.CharField()
    estatus = fields.BooleanField()
    fecha_alta = fields.DateTimeField()
    fecha_baja = fields.DateTimeField()
    dbreferencia = fields.ReferenceField(Cajero)


"""id_empleado = fields.ReferenceField(Empleado)

    @classmethod
    def find_by_username(cls, username: str):
        # def find_by_username(cls, username: str):
        try:
            user = Usuario.objects.get({'username': username})
            p = Cajero.objects.get({'_id': "5df8a21a3066665dc3fb05b8"})
            print(p.alias)
            user.cajero = p
        except Usuario.DoesNotExist:
            return {'message': f"No user with name:{ username }"}
        print(user)
        return user_schema.dump(user)
        # return {cls.query.filter_by(username=username).first()}
"""

"""
cajero = Cajero(alias="Cremas").save()
print(cajero.alias)
usuario = Usuario(username="Antonio", dbreferencia=cajero).save()
print(usuario.username, usuario.dbreferencia.alias)
# @classmethod
# def find_by_id(cls, _id: int) -> "Usuario":


def find_by_id(cls, _id: int):
        return cls.query.filter_by(id=_id).first()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
"""
