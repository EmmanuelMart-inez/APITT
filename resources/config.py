from bson.objectid import ObjectId
import datetime as dt

from flask_restful import Resource
from flask import request


import pymongo
from pymodm.errors import ValidationError
from pymongo.errors import DuplicateKeyError
from models.config import ConfigModel
from schemas.config import ConfigSchema

from datetime import *
from dateutil.relativedelta import *
import calendar
import dateutil.parser

# Get latest configuration of Loyalty's program
class Config(Resource):
    @classmethod
    def get(self):
        allconfig = ConfigModel.objects.all()
        allconfig_ordered_by_latest = allconfig.order_by([("fecha_creacion", pymongo.DESCENDING)])
        last_config = allconfig_ordered_by_latest.first()
        if not last_config:
            return {"Message": "No existe ninguna configuración"}, 404
        return ConfigSchema().dump(last_config), 200

    @classmethod
    def post(self):
        config_json = request.get_json()
        config = ConfigSchema().load(config_json)
        try:
            new_config = ConfigModel()
            if "equivalencia_punto_pesos" in config:
                new_config.equivalencia_punto_pesos = config["equivalencia_punto_pesos"]
            new_config.fecha_creacion = dt.datetime.now()
            new_config.save()
        except ValidationError as exc:
            print(exc.message)
            return {"message": "No se pudo crear la configuración"}, 400   
        return {'message': "configuración creada con éxito",
                '_id': str(new_config._id)
        }, 200

    @classmethod
    def put(self):
        config = ConfigModel.objects.all()
        config_ordered_by_latest = config.order_by([("fecha_creacion", pymongo.DESCENDING)])
        last_config = config_ordered_by_latest.first()
        config_json = request.get_json()
        new_config = ConfigSchema().load(config_json)
        try:
            if "equivalencia_punto_pesos" in new_config:
                last_config.equivalencia_punto_pesos = new_config["equivalencia_punto_pesos"]
            last_config.fecha_creacion = dt.datetime.now()
            last_config.save()
        except ValidationError as exc:
            print(exc.message)
            return {"message": "No se pudo actualizar la configuración enviada"}, 400   
        return {'message': "Configuración modificada",
                '_id': str(last_config._id)
        }, 200
