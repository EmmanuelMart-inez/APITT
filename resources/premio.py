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


from models.premio import PremioModel
from models.participante import ParticipanteModel
from models.producto import CatalogoModel

from schemas.premio import PremioSchema
from schemas.participante import ParticipanteSchema
from schemas.producto import CatalogoSchema
from marshmallow import pprint

participante_schema = ParticipanteSchema()

premio_schema = PremioSchema()
premio_schemas = PremioSchema(many=True)

# Establish a connection to the database.
connect("mongodb://localhost:27017/ej1")

# TODO: Crear premios y quemar premios
# TODO: Separar en una nueva clase los id de los participantes
#       que reciben la notificacion y la fecha de quemado
# TODO: Aplicar metodos de segmentación
# TODO: Puntos variables, diversos tipos de bonificación
class PremioList(Resource):
    @classmethod
    def get(self, id):
        part_id = ObjectId(id)
        try:
            participante_premios_id = PremioModel.objects.raw({'id_participante': part_id})
            premios = participante_premios_id
            # for item in premios:
                # pprint(item)
        except PremioModel.DoesNotExist:
            return {'message': f"No premios in participante with id{ id }"}
        # TODO: Agregar el URL para la solicitud al API de la notificacion, el link a la notificacion
        return {"Premios":
                    PremioSchema(
                    only=(
                        "_id",
                        "nombre", 
                        "puntos", 
                        "codigo_barras", 
                        "codigo_qr",
                        "imagen_icon",
                        "imagen_display",
                        "fecha_creacion", 
                        "fecha_vigencia", 
                        "fecha_redencion",
                        # "id_producto",
                        "id_participante"
                    ), many=True).dump(premios),
                },200


class Premio(Resource):
    @classmethod
    def post(self):
        premio_json = request.get_json()
        # print(premio_json)
        premio = premio_schema.load(premio_json )
        try:
            p = PremioModel(
                nombre=premio["nombre"],
                puntos=premio["puntos"],
                codigo_barras=premio["codigo_barras"],
                codigo_qr=premio["codigo_qr"],
                imagen_icon=premio["imagen_icon"],
                imagen_display=premio["imagen_display"],
                fecha_creacion=premio["fecha_creacion"],
                fecha_vigencia=premio["fecha_vigencia"],
                fecha_redencion=premio["fecha_redencion"],
                id_participante=premio["id_participante"]
            ).save()
        except ValidationError as exc:
            print(exc.message)
            return {"message": "No se pudo crear el nuevo premio."}   
        return {'message': "Premio creado",
                'ObjectId': PremioSchema(
                only=(
                "_id",
                )).dump(p)
        }, 200


    @classmethod
    def delete(self):
        pass