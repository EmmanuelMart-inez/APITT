import json
import datetime as dt
import functools
import uuid
from bson.objectid import ObjectId
import pymongo

from flask import request, jsonify
from flask_restful import Resource
from pymodm import connect, fields, MongoModel, EmbeddedMongoModel
from pymodm.errors import ValidationError
from pymongo.errors import DuplicateKeyError


from models.filtro import *
from models.participante import ParticipanteModel
from models.premio import PremioModel, PremioParticipanteModel
from models.venta import VentaModel
from models.encuesta import EncuestaModel, ParticipantesEncuestaModel
from models.tarjeta import TarjetaPuntosModel, TarjetaSellosModel

from schemas.participante import ParticipanteSchema
from models.encuesta import EncuestaModel, EncuestaPaginaModel, EncuestaOpcionesModel, ParticipantesEncuestaModel
from schemas.encuesta import EncuestaSchema, EncuestaPaginaSchema, EncuestaOpcionesSchema, ParticipanteEncuestaSchema
from marshmallow import pprint

# Establish a connection to the database.
connect("mongodb://localhost:27017/ej1")

# Filtrado de participantes para los que va dirigido el contenido (premio, encuesta, notificación)
class FiltradoByMetrica(Resource):
    @classmethod
    def post(self):
        req = request.get_json()
        filtersList = []
        try:
            for fi in req:
                idList = []
                if fi['document'] == 'participante_model_tarjeta_sellos':     
                    fi = switchFilter(TarjetaSellosModel, fi)
                    filterList = joinCollectionToParticipanteModel(ParticipanteModel, 'tarjeta_sellos', fi, filtersList, True, '$_id')
                elif fi['document'] == 'participante_model_tarjeta_puntos':     
                    fi = switchFilter(TarjetaPuntosModel, fi)
                    filterList = joinCollectionToParticipanteModel(ParticipanteModel, 'tarjeta_puntos', fi, filtersList, True, '$_id')
                elif fi['document'] == 'participante_model':         
                    fi = switchFilter(ParticipanteModel, fi) 
                    filtersList = formatResponseFilter(fi, filtersList)
                elif fi['document'] == 'participante_premio_model':         
                    fi = switchFilter(PremioParticipanteModel, fi)  
                    filtersList = formatResponseFilterByField(fi, filtersList, '$id_participante')
                elif fi['document'] == 'venta_model':        
                    fi = switchFilter(VentaModel, fi)  
                    filtersList = formatResponseFilterByField(fi, filtersList, '$id_participante')
                elif fi['document'] == 'encuesta_model':          
                    fi = switchFilter(EncuestaModel, fi)  
                    filterList = joinCollectionToParticipanteModel(ParticipantesEncuestaModel, 'id_encuesta', fi, filtersList, False, "$id_participante")
                elif fi['document'] == 'participantes_encuesta_model':       
                    fi = switchFilter(ParticipantesEncuestaModel, fi)            
                    filtersList = formatResponseFilterByField(fi, filtersList, "$id_participante")
            return  filtersList, 200
        except ParticipanteModel.DoesNotExist:
            return {'message': 'Ocurrió un error al procesar su petición'}, 500
        return {'message': 'Valor: IdMetrica invalido'}, 400



# simbols_number = ['> gt', '< lt', '!= .objects.exclude()', '<> range' '= exact']
# simbols_date = ['>', '<', '!=', '<>' '=']
# simbols_date_input = ['anterior lt', 'siguiente gt', 'actual exact'] # fecha, simbolo
# simbols_date_chunk = ['antes !!', 'despues !!', 'dia day', 'dias range day', 'semana', 'semanas week', 'mes', 'meses month', 'año year', 'años'] # simbolo_fecha, simbolo, escala
# simbols_date_rango = [ 'entre range'] # fecha(s),
# fecha(s), unidad_tiempo (si es '' default: día), cantidad, operador