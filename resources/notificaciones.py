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

from schemas.participante import ParticipanteSchema 
from models.participante import ParticipanteModel 
from schemas.notificacion import NotificacionSchema
from models.notificacion import NotificacionModel 
from marshmallow import pprint

participante_schema = ParticipanteSchema()
not_schema = NotificacionSchema()
not_schemas = NotificacionSchema(many=True)

# Establish a connection to the database.
connect("mongodb://localhost:27017/ej1")

class NotificacionList(Resource):
    @classmethod
    def get(self, id):
    #Participante id = part_id
        part_id = ObjectId(id)
        try:
            notifs = NotificacionModel.objects.get({'id_participante': part_id})
        except NotificacionModel.DoesNotExist:
            return {'message': f"No sellos_card in participante with id{ id }"}
        return not_schemas().dump(only=("_id"))
    
    @classmethod
    def post(self, id):
        part_id = ObjectId(id)
        try:
            notif = NotificacionModel(
                id_participante=part_id,
                titulo="Bienvenido al programa",
            ).save()
        except ValidationError as exc:
            print(exc.message)
            return {"message": "No se pudo crear la notificacion."} 
        return NotificacionSchema(
            only=(
            "_id",
            "titulo",
            "id_participante"
            )).dump(p), 200



