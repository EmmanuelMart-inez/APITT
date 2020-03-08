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


from models.premio import PremioModel, PremioParticipanteModel
from models.participante import ParticipanteModel
from models.producto import CatalogoModel

from schemas.premio import PremioSchema, PremioParticipanteSchema
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

            participante_premios = PremioParticipanteModel.objects.raw({'id_participante': part_id})
            pprint(participante_premios)
            premios=[]
            for premio in participante_premios: 
                premios.append(premio.id_premio)
                pprint(premio.id_premio)
            # premios = participante_premios_id
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

# Recurso del administrador
class PremioId(Resource):
    # Obtener un premio por id 
    @classmethod 
    def get(self, id):
        p = PremioModel.find_by_id(id)
        if not p:
            return {"message": "No se encontro el premio"}, 404
        return PremioSchema(
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
                    )).dump(p)
    # Test!
    # Actualizar el premio con el id dado
    @classmethod
    def patch(self, id):
        p = PremioModel.find_by_id(id)
        if not p:
            return {"message": "No se encontro la notificación asociada a este premio"}, 404
        p_req = request.get_json()
        premio = premio_schema.load(p_req["premio"])
        try:
            if "nombre" in premio:
                p.nombre = premio["nombre"] 
            if "puntos" in puntos:
                p.puntos = puntos["puntos"] 
            if "codigo_barras" in premio:
                p.codigo_barras = puntos["codigo_barras"] 
            if "codigo_qr" in premio:
                p.codigo_barras = puntos["codigo_barras"] 
            if "imagen_icon" in premio:
                p.imagen_icon = puntos["imagen_icon"] 
            if "imagen_display" in premio:
                p.imagen_icon = premio["imagen_icon"] 
            if "fecha_creacion" in premio:
                p.imagen_icon = premio["imagen_icon"] 
            if "fecha_vigencia" in premio:
                p.fecha_vigencia = premio["fecha_vigencia"] 
            if "fecha_redencion" in premio:
                p.fecha_redencion = premio["fecha_redencion"] 
            p.save()
        except ValidationError as exc:
            print(exc.message)
            return {"message": "No se pudo actualizar el premio."}, 400
        return {p}, 200


class Premio(Resource):
    @classmethod
    def post(self):
        premio_json = request.get_json()
        # print(premio_json)
        premio = premio_schema.load(premio_json )
        try:
            p = PremioModel()
            if "nombre" in premio:
                p.nombre=premio["nombre"]
            if "puntos" in premio:
                p.puntos=premio["puntos"]
            if "codigo_barras" in premio:
                p.codigo_barras=premio["codigo_barras"]
            if "codigo_qr" in premio:
                p.codigo_qr=premio["codigo_qr"]
            if "imagen_icon" in premio:
                p.imagen_icon=premio["imagen_icon"]
            if "imagen_display" in premio:
                p.imagen_display=premio["imagen_display"]
            if "fecha_creacion" in premio:
                p.fecha_creacion=premio["fecha_creacion"]
            if "fecha_vigencia" in premio:
                p.fecha_vigencia=premio["fecha_vigencia"]
            if "fecha_redencion" in premio:
                p.fecha_redencion=premio["fecha_redencion"]
            # if "id_participante" in premio:
            #     p.id_participante=premio["id_participante"]
            p.save()
            # Enviar a todos los participantes
            for participante in ParticipanteModel.objects.all():
                premio = PremioParticipanteModel(
                    id_premio = p._id,
                    id_participante = participante._id,
                    estado = 0
                ).save()
            
        except ValidationError as exc:
            p.delete()
            print(exc.message)
            return {"message": "No se pudo crear el nuevo premio o enviar a los participantes solicitados."}   
        return {'message': "Premio creado",
                'ObjectId': PremioSchema(
                only=(
                "_id",
                )).dump(p)
        }, 200


    @classmethod
    def delete(self):
        pass