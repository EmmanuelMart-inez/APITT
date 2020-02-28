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

    # Obtener todas las encuestas creadas
    @classmethod
    def get(self):
        try:
            encuestas = EncuestaModel.objects.all()
        except EncuestaModel.DoesNotExist:
            return {"message": "Encontró ninguna encuesta."}, 200   
        return EncuestaSchema(
                    only=(
                        "_id",
                        "categoria",
                        "fecha_creacion",
                        "fecha_respuesta",
                        "metrica",
                        "puntos",
                        "paginas",
                    ), many=True).dump(encuestas), 200

    # Crear encuesta 
    # Tentativamente enviar encuesta a todos los participantes
    # En un futuro añadir la segmentacion a este mmismo recurso dado que no se necesitan templates 
    # o por lo menos aun no se encuentra razones para necesitarlos
    @classmethod
    def post(self):
        encuesta_json = request.get_json()
        # pprint(encuesta_json)
        encuesta = EncuestaSchema().load(encuesta_json)
        try:
            e = EncuestaModel()
            if "titulo" in encuesta:
                e.titulo=encuesta["titulo"]
            if "categoria" in encuesta:
                e.categoria=encuesta["categoria"]
            e.fecha_creacion=dt.datetime.now()
            if "metrica" in encuesta:
                e.metrica=encuesta["metrica"]
            if "puntos" in encuesta:
                e.puntos=encuesta["puntos"]
            if "paginas" in encuesta:
                e.paginas=encuesta["paginas"]
                pprint(e.paginas)
                # for pagina in e.paginas:
                #     print(1)
            e.save()
            for participante in ParticipanteModel.objects.all():
                try:
                    # pprint(participante)
                    # pprint(encuesta)
                    encuestaParticipante = ParticipantesEncuestaModel(
                        id_participante=participante._id,
                        id_encuesta=e._id,
                        estado="sin responder"
                    ).save()
                except ValidationError as exc:
                    # eliminar los que fueron agregados
                    print(exc.message, exc)
                    return {"message": "No se pudo crear una nueva encuesta."}
        except ValidationError as exc:
            print(exc.message)
            return {"message": "No se pudo crear una nueva encuesta."}   
        return {'message': "Encuesta creada",
                'ObjectId': EncuestaSchema(
                only=(
                "_id",
                )).dump(e)
        }, 200

class AdministradorEncuestas(Resource):
    # Obtener el registro de todas las encuestas
    # responidadas
    @classmethod
    def get(self):
        try:
            participantes_encuestas = ParticipantesEncuestaModel.objects.all()
            # for index, pencuesta in enumerate(participantes_encuestas):
            #     pprint(str(pencuesta.id_encuesta))
        except ParticipantesEncuestaModel.DoesNotExist:
            return {"message": "Encontró ningún registro de encuesta, primero debe crear una encuesta para despues ser asignada en POST /controlencuestas."}, 200   
        return ParticipanteEncuestaSchema(
                    only=(
                        "_id",
                        "id_participante",
                        "id_encuesta",
                        "fecha_respuesta",
                        "estado",
                        "respuestas"
                    ), many=True).dump(participantes_encuestas), 200

class ControlEncuestas(Resource):
    
    # Enviar nuevas encuestas a participantes
    # NOTE: id_participanteencuesta = id_encuesta ___ Ojo: fix later!
    @classmethod
    def post(self, id_participanteencuesta):
        enc_id = ObjectId(id_participanteencuesta)
        try:
            encuesta = EncuestaModel.objects.get({'_id': enc_id})
            # for item in encuesta:
            #     pprint(item)
        except EncuestaModel.DoesNotExist:
            return {'message': f"No encuesta with participante with id{ id_participanteencuesta }"}, 504
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
                            fecha_creacion=dt.datetime.now()
                        ).save()
                    except ValidationError as exc:
                        # eliminar los que fueron agregados
                        print(exc.message, exc)
                        return {"message": "No se pudo crear una nueva encuesta."}
            except ParticipanteModel.DoesNotExist as exc:
                print(exc.message)
                return {"message": "No se encontro participantes."}
            return {"message": "Operación exitosa, participantes agregados a la encuesta",
            'info': ParticipanteEncuestaSchema(
                only=(
                "id_encuesta",
                "estado"
                )).dump(encuestaParticipante)
            }, 200
        else:
            # TODO: Regresar los datos del los participantes_encuestas para pruebas
            # TODO: Ajustar la fecha solo si el estado es respondido, en caso de eliminar dejar igual
            return {"message": "No ingreso un metodo de segmentación"}, 500 
        
    # Enviar formulario de encuesta
    @classmethod
    def patch(self, id_participanteencuesta):
        e_id = ObjectId(id_participanteencuesta)
        try:
            #_id de ParticipanteEncuestaModel 
            participante_encuesta = ParticipantesEncuestaModel.objects.get({'_id': e_id})
                # pprint(item)
        except EncuestaModel.DoesNotExist:
            return {'message': f"No ParticipanteEncuesta with id{ id_participanteencuesta }"}
        
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
                # "id_encuesta",
                # "id_participante",
                "estado"
                )).dump(participante_encuesta)
        }, 200

    # Consultar la respuesta de un participante a una encuesta por id: id_participanteencuesta
    @classmethod
    def get(self, id_participanteencuesta):
        resultado = ParticipantesEncuestaModel.find_by_id(id_participanteencuesta)
        if not resultado:
            return {"message": "No se encontro el registro de respuesta de encuesta que coincida con el id dado"}, 404
        return ParticipanteEncuestaSchema(
                    only=(
                        "_id",
                        "id_participante",
                        "id_encuesta",
                        "fecha_respuesta",
                        "estado",
                        "respuestas"
                    )).dump(resultado), 200


#  TODO: Refactorizar los metodos a 
    # /encuesta/id/participante/id
    # -> desencadenar la creacioón de todas las notificaciones
    # a los usuarios y tener una notificación única y una tabla
    # auxiliar con todos los datos de estas


class Respuestas(Resource):
    # Obtener información asociada a las encuestas y las respuestas que los participantes han de responder
    @classmethod
    def get(self, id_encuesta, id_participante):
        pass