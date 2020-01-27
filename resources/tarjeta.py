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
from schemas.tarjeta import TarjetaSellosSchema, TarjetaPuntosSchema
from marshmallow import pprint

participante_schema = ParticipanteSchema(many=True)
selloscard_schema = TarjetaSellosSchema()
puntoscard_schema = TarjetaPuntosSchema()
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
    
    """Busca la tarjeta de sellos del participante 
    con el _id dado en el URL"""
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

    """ Acumula los sellos en la tarjeta de sellos de un participante
        Si el # sellos + los que se desea poner es < total asignar, de lo contrario 
        poner el excedente y otorgarle un premio al participante y una notificación
    """
    @classmethod
    def patch(self, id):
        p = ParticipanteModel.find_by_id(id)
        if not p:
            return {'message': f"No participante with id:{ id }"}
        tarjeta_sellos_json = request.get_json()
        # print(user_json)
        tarjeta = TarjetaSellosSchema().load(tarjeta_sellos_json)
        # Validaciones
        print(p.tarjeta_sellos.num_sellos)
        print(tarjeta["num_sellos"])
        p.tarjeta_sellos.num_sellos = p.tarjeta_sellos.num_sellos +tarjeta["num_sellos"] 
        p.tarjeta_sellos.save()
        return {"_id": str(p._id), 
                "nombre": p.nombre,
                "num_sellos": p.tarjeta_sellos.num_sellos}, 200
        ## TODO: Generar notificación y premio, ademas de reiniciar la cuenta cuando se excede un límite

    """ Actualiza los sellos en la tarjeta de sellos de un participante
        Si el # sellos + los que se desea poner es < total asignar, de lo contrario 
        poner el excedente y otorgarle un premio al participante y una notificación
    """
    @classmethod
    def put(self, id):
        p = ParticipanteModel.find_by_id(id)
        if not p:
            return {'message': f"No participante with id:{ id }"}
        tarjeta_sellos_json = request.get_json()
        # print(user_json)
        tarjeta = TarjetaSellosSchema().load(tarjeta_sellos_json)
        # Validaciones
        print(p.tarjeta_sellos.num_sellos)
        print(tarjeta["num_sellos"])
        p.tarjeta_sellos.num_sellos = tarjeta["num_sellos"] 
        p.tarjeta_sellos.save()
        return {"_id": str(p._id), 
                "nombre": p.nombre,
                "num_sellos": p.tarjeta_sellos.num_sellos}, 200
        ## TODO: Generar notificación y premio, ademas de reiniciar la cuenta cuando se excede un límite
        

class TarjetaPuntos(Resource):
    """Busca una tarjeta de sellos 
    asociada a un ID de un participante"""
    @classmethod
    def get(self, id_participante):
        parti_id = ObjectId(id_participante)
        try:
            p = ParticipanteModel.objects.get({'_id': parti_id})
        except ParticipanteModel.DoesNotExist:
            return {'message': f"No participante with id{ id }"}
        return ParticipanteSchema(
            only=(
            "tarjeta_puntos",
            )).dump(p), 200

    """Añade una tarjeta de puntos al 
    participante con el _id = id_participante"""
    @classmethod
    def post(self, id_participante):
        parti_id = ObjectId(id_participante)
        try:
            p = ParticipanteModel.objects.get({'_id': parti_id})
        except ParticipanteModel.DoesNotExist:
            return {'message': f"No participante with id{ id }"}
        try: 
            puntos_card = TarjetaPuntosModel(
                balance = 10.0,
            ).save()
            p.tarjeta_puntos=puntos_card
            p.save()
        except ValidationError as exc:
            print(exc.message)
            return {"message": "No se pudo crear la tarjeta de puntos."} 
        return ParticipanteSchema(
            only=(
            "_id",
            "nombre",
            "tarjeta_puntos"
            )).dump(p), 200



    """Actualiza los puntos que tiene un participante
    con el _id = id_participante"""
    @classmethod
    def put(self, id_participante):
        tarjeta_puntos_json = request.get_json()
        print(tarjeta_puntos_json)
        tarjeta = puntoscard_schema.load(tarjeta_puntos_json)
        parti_id = ObjectId(id_participante)
        try:
            p = ParticipanteModel.objects.get({'_id': parti_id})
            card_id = p.tarjeta_puntos._id
        except ParticipanteModel.DoesNotExist:
            return {'message': f"No participante with id{ id }"}
        try:     
            card = TarjetaPuntosModel.objects.get({'_id': card_id})
            card.balance = tarjeta["balance"]
            card.save()
        except TarjetaPuntosModel.DoesNotExist:
            return {'message': f"Can't update tarjeta_puntos with id{ id }"}
        return {'saldo': 'Actualizado',
                'participante': ParticipanteSchema(
                    only=(
                    "_id",
                    "nombre",
                    "tarjeta_puntos"
                    )).dump(p),
                }, 200
