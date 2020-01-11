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


from models.participante import ParticipanteModel
from models.tarjeta import TarjetaSellosModel
from schemas.notificacion import NotificacionSchema
from models.notificacion import NotificacionModel 
from schemas.participante import ParticipanteSchema
from schemas.tarjeta import TarjetaSellosSchema
from marshmallow import pprint

participante_schema = ParticipanteSchema()
selloscard_schema = TarjetaSellosSchema()
not_schema = NotificacionSchema()
not_schemas = NotificacionSchema(many=True)
# user_schema = UserSchema()
# Establish a connection to the database.
connect("mongodb://localhost:27017/ej1")

class Participante(Resource):
    @classmethod
    def get(self, id):
        p = ParticipanteModel.find_by_id(id)
        if not p:
            return {"message": "No se encontro el usuario"}
        return ParticipanteSchema(
            only=(
            "_id",
            "nombre",
            "paterno",
            "password",
            "email",
            "foto",
            "fecha_nacimiento",
            "tarjeta_sellos", 
            "tarjeta_puntos",
            )).dump(p), 200

    @classmethod
    def put(self, id):
        p = ParticipanteModel.find_by_id(id)
        if not p:
            return {"message": "No se encontro el usuario"}
        user_json = request.get_json()
        # print(user_json)
        user = participante_schema.load(user_json)
        try:
            p.nombre=user["nombre"]
            p.password=user["password"]
            p.email=user["email"]
            p.foto=user["foto"]
            p.save()
        except ValidationError as exc:
            print(exc.message)
            return {"message": "No se pudo crear el nuevo participante."}
        return ParticipanteSchema(
            only=(
            "_id",
            "nombre",
            "password",
            "email",
            "foto",
            "fecha_nacimiento",
            "tarjeta_sellos", 
            "tarjeta_puntos",
            )).dump(p), 200
        
class ParticipanteList(Resource):
    @classmethod
    def post(self):
        user_json = request.get_json()
        print(user_json)
        user = participante_schema.load(user_json)
        try:
            p = ParticipanteModel(
                nombre=user["nombre"],
                paterno=user["paterno"],
                sexo=user["sexo"],
                password=user["password"],
                email=user["email"],
                fecha_nacimiento=user["fecha_nacimiento"],
                fecha_antiguedad=dt.datetime.now(),
                foto=user["foto"],
            ).save()
        except ValidationError as exc:
            print(exc.message)
            return {"message": "No se pudo crear el nuevo participante."}   
        return {'message': "Participante creado",
                'ObjectId': ParticipanteSchema(
                only=(
                "_id",
                )).dump(p)
        }, 200

        #return item.json(), 201
"""

    @classmethod
    def delete(self):
        pass

class ParticipanteList(Resource):
    def get(self):
        pass
"""


class WelcomeParticipante(Resource):
    @classmethod
    def get(self, id):
        p = ParticipanteModel.find_by_id(id)
        if not p:
            return {"message": "No se encontro el usuario"}
        try:
            part_id = ObjectId(id)
            participante_notifs_id = NotificacionModel.objects.raw({'id_participante': part_id})
            notifs = participante_notifs_id
            #for item in notifs:
                # pprint(item)
            total_notifs = notifs.count()
        except NotificacionModel.DoesNotExist:
            return {'message': f"No sellos_card in participante with id{ id }"}
        return {
            'Participante': ParticipanteSchema(
            only=(
            "_id",
            "nombre",
            "sexo",
            "tarjeta_sellos", 
            "tarjeta_puntos",
            )).dump(p),
            "total_notificaciones": total_notifs,
            }, 200