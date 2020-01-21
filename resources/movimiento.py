import json
import datetime as dt
import functools
import uuid
from bson.objectid import ObjectId
from flask import request
from flask_restful import Resource

from pymongo import TEXT
from pymongo.operations import IndexModel
from pymodm import connect, fields, MongoModel, EmbeddedMongoModel
from pymodm.errors import ValidationError
from pymongo.errors import DuplicateKeyError

#from schemas.participante import ParticipanteSchema 
#from models.participante import ParticipanteModel 
from schemas.movimiento import MovimientoAppSchema
from models.movimiento import MovimientoAppModel 
from marshmallow import pprint

# not_schema = NotificacionSchema()
# not_schemas = NotificacionSchema(many=True)

# Establish a connection to the database.
connect("mongodb://localhost:27017/ej1")

class MovimientoList(Resource):
    # Obtener los movimientos de un participante: APP
    @classmethod
    def get(self, id_participante):
        part_id = ObjectId(id_participante)
        try:
            participante_movimientos_id = MovimientoAppModel.objects.raw({'id_participante': part_id})
            movimientos = participante_movimientos_id
            # for item in premios:
                # pprint(item)
        except MovimientoAppModel.DoesNotExist:
            return {'message': f"No movimientos in participante with id{ id_participante }"}
        # TODO: Agregar el URL para la solicitud al API de la notificacion, el link a la notificacion
        return {"Movimientos":
                    MovimientoAppSchema(
                    only=(
                        "_id",
                        "id_participante",
                        "nombre",
                        "tipo",
                        "total",
                        "fecha",
                        "imagen_icon"
                    ), many=True).dump(movimientos),
                },200

    # Crear movimiento
    @classmethod
    def post(self, id_participante):
        mov_json = request.get_json()
        # print(premio_json)
        movimiento = MovimientoAppSchema().load(mov_json)
        try:
            p = MovimientoAppModel(
                id_participante=movimiento["id_participante"],
                nombre=movimiento["nombre"],
                tipo=movimiento["tipo"],
                total=movimiento["total"],
                fecha=movimiento["fecha"],
                imagen_icon=movimiento["imagen_icon"]                
            ).save()
        except ValidationError as exc:
            print(exc.message)
            return {"message": "No se pudo crear el nuevo movimiento."}   
        return {'message': "Movimiento creado",
                'ObjectId': MovimientoAppSchema(
                only=(
                "_id",
                )).dump(p)
        }, 200

    

class Movimiento(Resource): 
    # Eliminar el movimiento con el id_participante = id_movimiento
    @classmethod
    def delete(self, id_movimiento):
        mov_id = ObjectId(id_movimiento)
        try:
            mov = MovimientoAppModel.objects.get({'_id': mov_id})
            mov.delete()
        except MovimientoAppModel.DoesNotExist as exc:
            print(exc)
            return {"message": "No se pudo eliminar el movimiento, porque no existe."}, 504 
        return {"message": "Eliminado"}, 200


    # # Eliminar el movimiento con el id = id_movimiento y el participante dado
    # @classmethod
    # def delete(seld, id_participante, id_movimiento):
    #     pass

