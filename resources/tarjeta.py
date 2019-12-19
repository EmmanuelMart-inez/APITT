import json
import datetime as dt
import functools
import uuid
from bson.objectid import ObjectId
from flask import request
from flask_restful import Resource

from pymodm import connect, fields, MongoModel, EmbeddedMongoModel
from pymodm.errors import ValidationError
from pymongo.errors import DuplicateKeyError

from models.tarjeta import TarjetaPuntosModel, TarjetaSellosModel
from schemas.participante import ParticipanteSchema 
from models.participante import ParticipanteModel 
from schemas.tarjeta import TarjetaSellosSchema
from marshmallow import pprint

participante_schema = ParticipanteSchema(many=True)
selloscard_schema = TarjetaSellosSchema()
# user_schema = UserSchema()
# Establish a connection to the database.
connect("mongodb://localhost:27017/ej1")

class TarjetaSellos(Resource):
    @classmethod
    def post(self, id):
        parti_id = ObjectId(id)
        try:
            p = ParticipanteModel.objects.get({'_id': parti_id})
        except ParticipanteModel.DoesNotExist:
            return {'message': f"No participante with id{ id }"}
        datetoObjectId = dt.datetime.now() 
        descripcion_tarjeta = "Por cada bebida que compras acumulas una estrella, al acumular 8 bebidas te regalamos una!"
        try:
            selloscard = TarjetaSellosModel(
                num_sellos=0,
                descripcion=descripcion_tarjeta
            ).save()
            p.tarjeta_sellos=selloscard
            p.save()
        except ValidationError as exc:
            print(exc.message)
            return {"message": "No se pudo crear la tarjeta de sellos."} 
        return ParticipanteSchema(
            only=(
            "_id",
            "nombre",
            "tarjeta_sellos"
            )).dump(p), 200
    
    @classmethod
    def get(self, id):
        parti_id = ObjectId(id)
        try:
            p = ParticipanteModel.objects.get({'_id': parti_id})
        except ParticipanteModel.DoesNotExist:
            return {'message': f"No participante with id{ id }"}
        return ParticipanteSchema(
            only=(
            "_id",
            "nombre",
            "tarjeta_sellos"
            )).dump(p), 200


class ParticipanteList(Resource):
    @classmethod
    def post(self):
        user_json = request.get_json()
        print(user_json)
        user = participante_schema.load(user_json)
        try:
            ParticipanteModel(
                nombre=user["nombre"],
                paterno=user["paterno"],
                sexo=user["sexo"],
                password=user["password"],
                email=user["email"],
                fecha_nacimiento=user["fecha_nacimiento"],
                fecha_antiguedad=dt.datetime.now(),
                foto=user["foto"]
            ).save()
        except ValidationError as exc:
            print(exc)
            return {"message": "ValidationError '{}'".format(errors=exc.message)}
        return {'message': "Participante creado"}, 200
