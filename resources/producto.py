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

from schemas.producto import CatalogoSchema
from models.producto import CatalogoModel  
from marshmallow import pprint

cat_schema = CatalogoSchema()
cats_schema = CatalogoSchema(many=True)

# Establish a connection to the database.
connect("mongodb://localhost:27017/ej1")

#TODO: Añadir Encuestas link
class CatalogoList(Resource):
    
    #TODO: Refactorizar llamando a metodos DAO de la clase modelo
    @classmethod
    def get(self):
        try:
            catalogo = CatalogoModel.objects.all()
            #for item in notifs:
            #    pprint(item)
        except CatalogoModel.DoesNotExist:
            return {'message': "No se encontro resultados que coincidan con su busqueda"}
        # TODO: Agregar el URL para la solicitud al API del producto para generar pedido, el link para personalizarla
        return {"Catalogo":
                    CatalogoSchema(
                    only=(
                    "_id", 
                    "tipo", 
                    "imagen", 
                    "titulo", 
                    "descripcion", 
                    "fecha_vigencia",
                    ), many=True).dump(catalogo),
                },200

     #TODO: Refactorizar llamando a metodos DAO de la clase modelo
    @classmethod
    def post(self):
        catalog_product_json = request.get_json()
        print(catalog_product_json)
        cat = cat_schema.load(catalog_product_json)
        print("loaded")
        try:
            catalog_product = CatalogoModel(
                tipo = cat["tipo"],
                imagen = cat["imagen"],
                titulo = cat["titulo"],
                descripcion = cat["descripcion"],
                fecha_vigencia = cat["fecha_vigencia"],
            ).save()
            print("guardado")
        except ValidationError as exc:
            print(exc.message)
            return {"message": "No se pudo crear el producto."}
        return {"message": "Producto guardado en el catálogo con éxito.",
                "_id": CatalogoSchema(only=("_id",)).dump(catalog_product)},200


class Catalogo(Resource):
    @classmethod
    def get(self, vartipo):
        try:
            catalogo = CatalogoModel.objects.raw({'tipo': vartipo})
            #for item in notifs:
            #    pprint(item)
        except CatalogoModel.DoesNotExist:
            return {'message': "No se encontro resultados que coincidan con su busqueda"}
        # TODO: Agregar el URL para la solicitud al API del producto para generar pedido, el link para personalizarla
        return {"Catalogo":
                    CatalogoSchema(
                    only=(
                    "_id", 
                    "tipo", 
                    "imagen", 
                    "titulo", 
                    "descripcion", 
                    "fecha_vigencia",
                    ), many=True).dump(catalogo),
                },200