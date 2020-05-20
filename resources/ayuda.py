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

from schemas.ayuda import AyudaSchema
from models.ayuda import AyudaModel
from marshmallow import pprint

ayuda_schema = AyudaSchema()
ayuda_schemas = AyudaSchema(many=True)

# Establish a connection to the database.
connect("mongodb://localhost:27017/ej1")

class AyudaList(Resource):
    @classmethod
    def get(self):
        try:
            ayudas = AyudaModel.objects.all()
            # for item in premios:
                # pprint(item)
        except AyudaModel.DoesNotExist:
            return {'message': f"No ayuda in seccion ayuda"}
        # TODO: Agregar el URL para la solicitud al API de la notificacion, el link a la notificacion
        return {"Ayuda":
                    AyudaSchema(
                    only=(
                            "_id",
                            "imagen_icon",
                            "titulo",
                            "descripcion",
                    ), many=True).dump(ayudas),
                },200

    @classmethod
    def post(self):
        item_json = request.get_json()
        # print(premio_json)
        item = ayuda_schema.load(item_json)
        try:
            item = AyudaModel(
                imagen_icon=item["imagen_icon"],
                titulo=item["titulo"],
                descripcion=item["descripcion"]
            ).save()
        except ValidationError as exc:
            print(exc.message)
            return {"message": "No se pudo crear el item"}   
        return {'message': "Elemento creado",
                'ObjectId': AyudaSchema(
                only=(
                "_id",
                )).dump(item)
        }, 200

class Ayuda(Resource):
    @classmethod
    def delete(self, id):
        item = AyudaModel.find_by_id(id)
        if not item:
            return {"message": "No existe el elemento que desea eliminar"}, 404
        try:
            item.delete()
        except:
            return {"message":"Error: No se pudo eliminar"}, 500
        return {"message": "Eliminado satisfactoriamente"}, 200

    """
        Actualizar los datos de un elemento de la sección de ayuda en el front Web
    """
    @classmethod
    def put(self, id):
        a = AyudaModel.find_by_id(id)
        if not a:
            return {"message": "No existe el elemento que desea eliminar"}, 404
        a_req = request.get_json()
        ayuda = ayuda_schema.load(a_req)
        try:
            if "titulo" in ayuda:
                a.titulo = ayuda["titulo"] 
            if "descripcion" in ayuda:
                a.descripcion = ayuda["descripcion"] 
            if "imagen_icon" in ayuda:
                a.imagen_icon = ayuda["imagen_icon"] 
            a.save()
        except ValidationError as exc:
            print(exc.message)
            return {"message": "No se pudo actualizar el elemento de ayuda."}, 400
        return {"Actualizado exitosamente": AyudaSchema().dump(a)}, 200
        