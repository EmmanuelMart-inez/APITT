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
from schemas.participante import ParticipanteSchema
from models.encuesta import EncuestaModel, EncuestaPaginaModel, EncuestaOpcionesModel, ParticipantesEncuestaModel
from schemas.encuesta import EncuestaSchema, EncuestaPaginaSchema, EncuestaOpcionesSchema, ParticipanteEncuestaSchema
from marshmallow import pprint

participante_schema = ParticipanteSchema()

# user_schema = UserSchema()
# Establish a connection to the database.
connect("mongodb://localhost:27017/ej1")


class EncuestaParticipante(Resource):
    # Encuesta completa lista para pintar el cuestionario en el app
    @classmethod
    def get(self, id_encuesta):
        part_id = ObjectId(id_encuesta)
        print(id_encuesta)
        try:
            participante_encuestas_id = EncuestaModel.objects.get({'_id': part_id})
            encuesta = participante_encuestas_id
            for item in encuesta:
                pprint(item)
        except EncuestaModel.DoesNotExist:
            return {'message': f"No encuesta with participante with id{ id_encuesta }"}, 504
        return EncuestaSchema(
                    only=(
                        "_id",
                        "categoria",
                        "fecha_creacion",
                        "fecha_respuesta",
                        "metrica",
                        "puntos",
                        "paginas",
                    )).dump(encuesta), 200


    # Quemar o eliminar encuesta, por caducidad, segun sea el envio en el body
    @classmethod
    def patch(self, id_encuesta):
        pass

class Encuesta(Resource):
    # TODO: Segmentación
    # TODO: Hacer opcionales los campos como ya antes lo habia hecho con algun endpoint

    # Crear encuesta
    @classmethod
    def post(self):
        encuesta_json = request.get_json()
        # pprint(encuesta_json)
        encuesta = EncuestaSchema().load(encuesta_json)
        try:
            e = EncuestaModel(
                titulo=encuesta["titulo"],
                categoria=encuesta["categoria"],
                fecha_creacion=dt.datetime.now(),
                metrica=encuesta["metrica"],
                puntos=encuesta["puntos"],
                paginas=encuesta["paginas"]
            ).save()
        except ValidationError as exc:
            print(exc.message)
            return {"message": "No se pudo crear una nueva encuesta."}   
        return {'message': "Encuesta creada",
                'ObjectId': EncuestaSchema(
                only=(
                "_id",
                )).dump(e)
        }, 200

class ControlEncuestas(Resource):
    # Enviar nuevas encuestas a participantes
    @classmethod
    def post(self, id_encuesta):
        enc_id = ObjectId(id_encuesta)
        try:
            encuesta = EncuestaModel.objects.get({'_id': enc_id})
            # for item in encuesta:
            #     pprint(item)
        except EncuestaModel.DoesNotExist:
            return {'message': f"No encuesta with participante with id{ id_encuesta }"}, 504
        segmentacion = request.get_json()
        print(segmentacion)
        if(segmentacion["filtro"] == "todos"):
            try:
                pall = ParticipanteModel.objects.all()
                for participante in pall:
                    try:
                        # pprint(participante)
                        # pprint(encuesta)
                        encuestaParticipante = ParticipantesEncuestaModel(
                            id_participante=participante._id,
                            id_encuesta=encuesta._id,
                            estado="sin responder",
                            fecha_respuesta=dt.datetime.now()
                        ).save()
                    except ValidationError as exc:
                        # eliminar los que fueron agregados
                        print(exc.message, exc)
                        return {"message": "No se pudo crear una nueva encuesta."}
            except ParticipanteModel.DoesNotExist as exc:
                print(exc.message)
                return {"message": "No se encontro participantes."}
            return {"message": "Operación exitosa, participantes agregados a la encuesta"}, 200
        else:
            return {"message": "No ingreso un metodo de segmentación"}, 500 
        
    # Enviar formulario de encuesta
    @classmethod
    def patch(self, id_encuesta):
        e_id = ObjectId(id_encuesta)
        try:
            #_id de ParticipanteEncuestaModel 
            participante_encuesta = ParticipantesEncuestaModel.objects.get({'_id': e_id})
                # pprint(item)
        except EncuestaModel.DoesNotExist:
            return {'message': f"No encuesta with id{ id_encuesta }"}
        
        respuesta_json = request.get_json()
        respuesta = ParticipanteEncuestaSchema().load(respuesta_json)
        try:
            participante_encuesta.fecha_respuesta = dt.datetime.now()
            participante_encuesta.estado = respuesta["estado"]
            participante_encuesta.respuestas = respuesta["respuestas"]
            participante_encuesta.save()
        except ValidationError as exc:
            print(exc.message)
            return {"message": "No se pudo crear la responder esta encuesta."}   
        return {'message': "Encuesta respondida satisfactoriamente",
                'info': ParticipanteEncuestaSchema(
                only=(
                "_id",
                "estado"
                )).dump(participante_encuesta)
        }, 200

