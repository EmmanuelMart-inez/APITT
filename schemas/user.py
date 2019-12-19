import sys
import json

# from packaging import version

from ma import ma
from marshmallow import Schema, fields, ValidationError

# from schemas.participante import Participante, FacebookFields, GoogleFields
# from schemas.empleado import Usuario


class EmpSchema(ma.Schema):
    _id = fields.Str()
    alias = fields.Str()

    class Meta:
        fields = ("_id", "alias")


class UserSchema(ma.Schema):
    _id = fields.Str()
    username = fields.Str()
    password = fields.Str()
    dbreferencia = fields.Nested(EmpSchema)

    # model = UserModel
    # load_only = ("password",)
    # dump_only = ("id",)
    # Fields to expose

    class Meta:
        fields = ("_id", "password", "username", "dbreferencia")


"""
user = Usuario(username="Monty", db)
blog = Blog(title="Something Completely Different", author=user)
result = BlogSchema().dump(blog)
pprint(result)
"""
