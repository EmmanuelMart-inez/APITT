import json
import datetime
import functools
import uuid
from bson.objectid import ObjectId

from flask import request, url_for, g
from flask_restful import Resource
from flask_jwt_extended import create_access_token, create_refresh_token
#from models.empleado import Usuario, Cajero
#from schemas.user import UserSchema, EmpSchema
from oa import facebook


from flask import jsonify
from flask_pymongo import PyMongo
from flask_marshmallow import Marshmallow

from ma import ma
from pymodm import MongoModel, EmbeddedMongoModel, fields, connect
from pymodm.errors import ValidationError
from pymongo.errors import DuplicateKeyError

from models.empleado import Empleado, Usuario, Cajero
from schemas.user import UserSchema, EmpSchema

user_schema = UserSchema()
# user_schema = UserSchema()
# Establish a connection to the database.
connect("mongodb://localhost:27017/ej1")


class FacebookLogin(Resource):
    @classmethod
    def get(cls):
        return facebook.authorize(
            callback=url_for("facebook.authorize", _external=True)
        )


# Get authorization
# Create user
# Save github token to user
# Create access token
# Return JWT
# Tokengetter will then use the current user to load token from database
class FacebookAuthorize(Resource):
    @classmethod
    def get(cls):
        resp = facebook.authorized_response()
        if resp is None or resp.get("access_token") is None:
            error_response = {
                "error": request.args["error"],
                "error_description": request.args["error_description"],
            }
            return error_response

        g.access_token = resp["access_token"]
        facebook_user = facebook.get(
            "/me?fields=id,name,birthday,last_name,email,gender"
        )  # this uses the access_token from the tokengetter function
        facebook_username = facebook_user.data["name"]

        print(facebook_user)
        print(facebook_user.data)
        print(facebook_user.data["name"])

        print(facebook_username == "Emmanuel Martínez Cerón")
        print(type(facebook_username))
        try:
            myuser = Usuario.objects.get({'username': facebook_username})
            user = UserSchema().dump(myuser)
            print(str(myuser._id))
        except Usuario.DoesNotExist:
            return {"message": "No se encontro el usuario"}
        #return {"message": "Encontrado"}

        access_token = create_access_token(identity=user['_id'], fresh=True)
        refresh_token = create_refresh_token(user['_id'])

        return {"access_token": access_token, "refresh_token": refresh_token}, 200

