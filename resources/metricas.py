import json
import datetime as dt
import functools
import uuid
from bson.objectid import ObjectId

from flask import request, jsonify
from flask_restful import Resource
from pymodm import connect, fields, MongoModel, EmbeddedMongoModel
from pymodm.errors import ValidationError
from pymongo.errors import DuplicateKeyError


from models.participante import ParticipanteModel
from schemas.participante import ParticipanteSchema
from models.encuesta import EncuestaModel, EncuestaPaginaModel, EncuestaOpcionesModel, ParticipantesEncuestaModel
from schemas.encuesta import EncuestaSchema, EncuestaPaginaSchema, EncuestaOpcionesSchema, ParticipanteEncuestaSchema
from marshmallow import pprint

# Establish a connection to the database.
connect("mongodb://localhost:27017/ej1")

simbols_number = ['> gt', '< lt', '!= .objects.exclude()', '<> range' '= exact']
# simbols_date = ['>', '<', '!=', '<>' '=']
simbols_date_input = ['anterior lt', 'siguiente gt', 'actual exact'] # fecha, simbolo
simbols_date_chunk = ['antes !!', 'despues !!', 'dia day', 'dias range day', 'semana', 'semanas week', 'mes', 'meses month', 'año year', 'años'] # simbolo_fecha, simbolo, escala
simbols_date_rango = [ 'entre range'] # fecha(s),
    # fecha(s), unidad_tiempo (si es '' default: día), cantidad, operador

# Filtrado de participantes para los que va dirigido el contenido (premio, encuesta, notificación)
class FiltradoByMetrica(Resource):
# class ParticipanteFiltradoByMetrica(Resource):
    @classmethod
    def get(self, idMetrica):
        req = request.get_json()
        # ps = ParticipanteModel.filter_by_date_range(req["date_start"], req["date_end"])
        # ps = ParticipanteModel.filter_by_dateExample(req["date_start"])
        
        # Número de participantes nuevos
        if idMetrica == '1': 
            try:
                if 'date_end' in req:
                    participantes_nuevos = ParticipanteModel.filter_by_date_range(req['date_start'], req['date_end'], req['field'])
                else:
                    participantes_nuevos = ParticipanteModel.filter_by_date(req['date_start'], req['tipo'], req['scale'], req['scale_value'], req['field'])
                idList = []
                for p in participantes_nuevos:
                    idList.append(str(p._id))
                return {
                    "participantes" : idList,
                    "total": len(idList),
                    }, 200
            except ParticipanteModel.DoesNotExist:
                return {'message': 'Ocurrió un error al procesar su petición'}, 500
        return {'message': 'Valor: IdMetrica invalido'}, 400
            