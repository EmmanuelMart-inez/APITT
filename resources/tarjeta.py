import json
import datetime as dt
import functools
import uuid
from bson.objectid import ObjectId
from flask import request
from flask_restful import Resource

import pymongo
from pymodm import connect, fields, MongoModel, EmbeddedMongoModel
from pymodm.errors import ValidationError
from pymongo.errors import DuplicateKeyError

from models.tarjeta import TarjetaPuntosModel, TarjetaSellosModel, TarjetaPuntosTemplateModel
from schemas.participante import ParticipanteSchema 
from models.participante import ParticipanteModel 
from schemas.tarjeta import  TarjetaSellosTemplateSchema, TarjetaSellosSchema, TarjetaPuntosSchema, TarjetaPuntosTemplateSchema
from marshmallow import pprint

participante_schema = ParticipanteSchema(many=True)
selloscard_schema = TarjetaSellosSchema()
selloscard_template_schema = TarjetaSellosTemplateSchema()
puntoscard_schema = TarjetaPuntosSchema()
puntoscard_template_schema = TarjetaPuntosTemplateSchema()
# user_schema = UserSchema()
# Establish a connection to the database.
connect("mongodb://localhost:27017/ej1")

# Para la administración de los niveles de puntos
class SistemaPuntos(Resource):
    @classmethod
    def post(self):
        tarjeta_json = request.get_json()
        tarjeta = puntoscard_template_schema.load(tarjeta_json)
        try:
            new_tarjeta = TarjetaPuntosTemplateModel()
            if "titulo" in tarjeta:
                new_tarjeta.titulo = tarjeta["titulo"]
            if "num_puntos" in tarjeta:
                new_tarjeta.num_puntos = tarjeta["num_puntos"]
            if "dias_vigencia" in tarjeta:
                new_tarjeta.dias_vigencia = tarjeta["dias_vigencia"]
            if "max_canjeos" in tarjeta:
                new_tarjeta.max_canjeos = tarjeta["max_canjeos"]
            if "id_notificacion" in tarjeta:
                new_tarjeta.id_notificacion = tarjeta["id_notificacion"]
            if "id_promocion" in tarjeta:
                new_tarjeta.id_promocion = tarjeta["id_promocion"]
            new_tarjeta.fecha_creacion = dt.datetime.now()
            new_tarjeta.save()
        except ValidationError as exc:
            print(exc.message)
            return {"message": "No se pudo crear el nivel"}, 400   
        return {'message': "Nivel creado",
                'ObjectId': TarjetaPuntosTemplateSchema(
                only=(
                "_id",
                )).dump(new_tarjeta)
        }, 200

    @classmethod
    def get(self):
        niveles = TarjetaPuntosTemplateModel.objects.all()
        if not niveles:
            return {"message": "No se encontró ningún nivel"}, 404
        return TarjetaPuntosTemplateSchema(many=True).dump(niveles)

class SistemaPuntosId(Resource):
    @classmethod
    def delete(self, id):
        nivel = TarjetaPuntosTemplateModel.find_by_id(id)
        if not nivel: 
            return {"message": "Error: No se encontró ningún nivel"}, 404
        try: 
            nivel.delete()
        except: 
            return {"message": "Error: No se pudo eliminar"}    
        return {"message": "Nivel eliminado"}

class TarjetaSellosTemplate(Resource):
    @classmethod
    def get(self):
        allcards = TarjetaSellosModel.objects.all()
        allconfig_ordered_by_latest = allcards.order_by([("fecha_creacion", pymongo.DESCENDING)])
        last_config = allconfig_ordered_by_latest.first()
        if not last_config:
            return {"Message": "No existe ninguna tarjeta de sellos activa"}, 404
        return TarjetaSellosTemplateSchema().dump(last_config), 200

    @classmethod
    def post(self):
        tarjeta_json = request.get_json()
        tarjeta = selloscard_template_schema.load(tarjeta_json)
        try:
            new_tarjeta = TarjetaSellosModel()
            if "fecha_inicio" in tarjeta:
                new_tarjeta.fecha_inicio = tarjeta["fecha_inicio"]
            if "fecha_fin" in tarjeta:
                new_tarjeta.fecha_fin = tarjeta["fecha_fin"]
            if "num_sellos" in tarjeta:
                new_tarjeta.num_sellos = tarjeta["num_sellos"]
            if "titulo" in tarjeta:
                new_tarjeta.titulo = tarjeta["titulo"]
            if "descripcion" in tarjeta:
                new_tarjeta.descripcion = tarjeta["descripcion"]
            if "icono_off" in tarjeta:
                new_tarjeta.icono_off = tarjeta["icono_off"]
            if "icono_on" in tarjeta:
                new_tarjeta.icono_on = tarjeta["icono_on"]
            if "producto" in tarjeta:
                new_tarjeta.producto = tarjeta["producto"]
            if "id_notificacion" in tarjeta:
                new_tarjeta.id_notificacion = tarjeta["id_notificacion"]
            if "id_promocion" in tarjeta:
                new_tarjeta.id_promocion = tarjeta["id_promocion"]
            if "trigger" in tarjeta:
                new_tarjeta.trigger = tarjeta["trigger"]
            if "cantidad_trigger" in tarjeta:
                new_tarjeta.cantidad_trigger = tarjeta["cantidad_trigger"]
            new_tarjeta.fecha_creacion = dt.datetime.now()
            new_tarjeta.save()
        except ValidationError as exc:
            print(exc.message)
            return {"message": "No se pudo crear la tarjeta"}, 400   
        return {'message': "Tarjeta creada",
                'ObjectId': TarjetaSellosTemplateSchema(
                only=(
                "_id",
                )).dump(new_tarjeta)
        }, 200

    @classmethod
    def put(self):
        cards = TarjetaSellosModel.objects.all()
        cards_ordered_by_latest = cards.order_by([("fecha_creacion", pymongo.DESCENDING)])
        last_card = cards_ordered_by_latest.first()
        # pprint(last_card)
        tarjeta_json = request.get_json()
        tarjeta = selloscard_template_schema.load(tarjeta_json)
        try:
            if "fecha_inicio" in tarjeta:
                last_card.fecha_inicio = tarjeta["fecha_inicio"]
            if "fecha_fin" in tarjeta:
                last_card.fecha_fin = tarjeta["fecha_fin"]
            if "num_sellos" in tarjeta:
                last_card.num_sellos = tarjeta["num_sellos"]
            if "titulo" in tarjeta:
                last_card.titulo = tarjeta["titulo"]
            if "descripcion" in tarjeta:
                last_card.descripcion = tarjeta["descripcion"]
            if "icono_off" in tarjeta:
                last_card.icono_off = tarjeta["icono_off"]
            if "icono_on" in tarjeta:
                last_card.icono_on = tarjeta["icono_on"]
            if "producto" in tarjeta:
                last_card.producto = tarjeta["producto"]
            if "id_notificacion" in tarjeta:
                last_card.id_notificacion = tarjeta["id_notificacion"]
            if "id_promocion" in tarjeta:
                last_card.id_promocion = tarjeta["id_promocion"]
            if "cantidad_trigger" in tarjeta:
                last_card.cantidad_trigger = tarjeta["cantidad_trigger"]
            if "trigger" in tarjeta:
                last_card.trigger = tarjeta["trigger"]
            last_card.fecha_creacion = dt.datetime.now()
            last_card.save()
        except ValidationError as exc:
            print(exc.message)
            return {"message": "No se pudo crear la tarjeta"}, 400   
        return {'message': "Tarjeta modificada",
                'ObjectId': TarjetaSellosTemplateSchema(
                only=(
                "_id",
                )).dump(last_card)
        }, 200

# Los siguentes endpoints crean tarjetas únicas para cada participante, no una general
class TarjetaSellos(Resource):
    @classmethod
    def post(self, id):
        parti_id = ObjectId(id)
        try:
            p = ParticipanteModel.objects.get({'_id': parti_id})
        except ParticipanteModel.DoesNotExist:
            return {'message': f"No participante with id{ id }"}, 404
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
            return {"message": "No se pudo crear la tarjeta de sellos."}, 404 
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
            return {'message': f"No participante with id{ id }"},404
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
            return {'message': f"No participante with id:{ id }"}, 404
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
            return {'message': f"No participante with id:{ id }"}, 404
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
            return {'message': f"No participante with id{ id }"}, 404
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
            return {'message': f"No participante with id{ id }"}, 404
        try: 
            puntos_card = TarjetaPuntosModel(
                balance = 10.0,
            ).save()
            p.tarjeta_puntos=puntos_card
            p.save()
        except ValidationError as exc:
            print(exc.message)
            return {"message": "No se pudo crear la tarjeta de puntos."}, 400 
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
            return {'message': f"No participante with id{ id }"}, 400 
        try:     
            card = TarjetaPuntosModel.objects.get({'_id': card_id})
            card.balance = tarjeta["balance"]
            card.save()
        except TarjetaPuntosModel.DoesNotExist:
            return {'message': f"Can't update tarjeta_puntos with id{ id }"}, 404
        return {'saldo': 'Actualizado',
                'participante': ParticipanteSchema(
                    only=(
                    "_id",
                    "nombre",
                    "tarjeta_puntos"
                    )).dump(p),
                }, 200
