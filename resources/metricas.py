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

productos = [
    {
        "_id" : "1",
        "nombre" : "bubbleTea",
        "precio_venta" : 55,
        "precio_compra" : 30,
        "categoria" : "Bebidas"
    },
    {
        "_id" : "2",
        "nombre" : "Bolipán",
        "precio_venta" : 20,
        "precio_compra" : 10,
        "categoria" : "Alimentos"
    },
    {
        "_id" : "3",
        "nombre" : "Café",
        "precio_venta" : 25,
        "precio_compra" : 10,
        "categoria" : "Bebidas"
    }
]

promociones = [
	{
		"_id": '1',
		"titulo": "BubbleCombo",
		"tipo": "gratis",
		"valor": 100.0,
		"productos_validos": ["1"],
		"fecha_vigencia":  "2029-06-06T16:00:00Z",
        "puntos": 0.0,
        "sellos": 0
	},
	{
		"_id": "2",
		"titulo": "50% de descuento sobre tu compra",
		"tipo": "porcentaje compra",
		"valor": 50.0,
		"productos_validos": ["1","3"],
		"fecha_vigencia":  "2020-06-06T16:00:00Z",
        "puntos": 0.0,
        "sellos": 0
	},
    {
		"_id": "3",
		"titulo": "2x1 en bolipanes",
		"tipo": "2", # --> 2x1  2
		"valor": 1.0,  #          1
		"productos_validos": ["2"],
		"fecha_vigencia":  "2020-06-06T16:00:00Z",
        "puntos": 0.0,
        "sellos": 0
	},
    {
		"_id": "4",
		"titulo": "3x2 en café",
		"tipo": "3", # --> 2x1  2
		"valor": 2.0,  #          1
		"productos_validos": ["3"],
		"fecha_vigencia":  "2020-06-06T16:00:00Z",
        "puntos": 0.0,
        "sellos": 0
	}
]

tickets = [
    {
		"_id": "1",
		"total": 80.00,
        "descuento": 20.0, #porcentaje
		"fecha": "2019-06-06T10:00:00Z",
		"id_participante": "5e599aacf97a00a6036b17ae",
		# forma_pago: {
		# 			nombre: "efectivo", 
		# 			otros_detalles: "Datos de la terminal importantes"
		# 			},
		# qr: "asdaqwke923jl4jql0jqeqeq",
		# descuento_general: 15.5,
		# usuario_id_usuario: usuario__id,
        "promociones": ["1", "2"],
		"detalle_venta": [
						{
							"cantidad": 2, 
							"impuestos": 0.16,
							"descuento_producto": 50.0,
							"producto": 	{
                                            "_id" : "2",
                                            "nombre" : "Bolipán",
                                            "precio_venta" : 20.0,
                                            "precio_compra" : 10.0,
                                            "categoria" : "Alimentos"
                                        },
							"importe": 20
					    },
                        {
							"cantidad": 2, 
							"impuestos": 0.16,
							"descuento_producto": 0.00,
							"producto": 	
                                        {
                                            "_id" : "1",
                                            "nombre" : "bubbleTea",
                                            "precio_venta" : 55.0,
                                            "precio_compra" : 30.0,
                                            "categoria" : "Bebidas"
                                        },
							"importe": 0.0
					    }
					   ]
    },
    {
		"_id": "2",
		"total": 80.0,
        "descuento": 20.0, #porcentaje
		"fecha": "2020-06-06T10:00:00Z",
		"id_participante": "5e599aacf97a00a6036b17ad",
		# forma_pago: {
		# 			nombre: "efectivo", 
		# 			otros_detalles: "Datos de la terminal importantes"
		# 			},
		# qr: "asdaqwke923jl4jql0jqeqeq",
		# descuento_general: 15.5,
		# usuario_id_usuario: usuario__id,
        "promociones": [],
		"detalle_venta": [
						{
							"cantidad": 1, 
							"impuestos": 0.16,
							"descuento_producto": 0.00,
							"producto": 	{
                                            "_id" : "2",
                                            "nombre" : "Bolipán",
                                            "precio_venta" : 20.0,
                                            "precio_compra" : 10.0,
                                            "categoria" : "Alimentos"
                                        },
							"importe": 80
					    }
					   ]
    },
    {
		"_id": "3",
		"total": 80.0,
        "descuento": 20.0, #porcentaje
		"fecha": "2020-06-06T10:00:00Z",
		"id_participante": "5e599aacf97a00a6036b17ae",
		# forma_pago: {
		# 			nombre: "efectivo", 
		# 			otros_detalles: "Datos de la terminal importantes"
		# 			},
		# qr: "asdaqwke923jl4jql0jqeqeq",
		# descuento_general: 15.5,
		# usuario_id_usuario: usuario__id,
        "promociones": [3,4],
		"detalle_venta": [
						{
							"cantidad": 1, 
							"impuestos": 0.16,
							"descuento_producto": 0.00,
							"producto": 	{
                                            "_id" : "2",
                                            "nombre" : "Bolipán",
                                            "precio_venta" : 20.0,
                                            "precio_compra" : 10.0,
                                            "categoria" : "Alimentos"
                                        },
							"importe": 80
					    },
                        {
                            "cantidad": 3, 
							"impuestos": 0.16,
							"descuento_producto": 0.00,
							"producto": 	{
                                                "_id" : "3",
                                                "nombre" : "Café",
                                                "precio_venta" : 25,
                                                "precio_compra" : 10,
                                                "categoria" : "Bebidas"
                                            },
							"importe": 50
                        }
					   ]
    },
    {
		"_id": "4",
		"total": 80.0,
        "descuento": 20.0, #porcentaje
		"fecha": "2020-07-06T10:00:00Z",
		"id_participante": "5e599aacf97a00a6036b17af",
		# forma_pago: {
		# 			nombre: "efectivo", 
		# 			otros_detalles: "Datos de la terminal importantes"
		# 			},
		# qr: "asdaqwke923jl4jql0jqeqeq",
		# descuento_general: 15.5,
		# usuario_id_usuario: usuario__id,
        "promociones": [3,4],
		"detalle_venta": [
						{
							"cantidad": 1, 
							"impuestos": 0.16,
							"descuento_producto": 0.00,
							"producto": 	{
                                            "_id" : "2",
                                            "nombre" : "Bolipán",
                                            "precio_venta" : 20.0,
                                            "precio_compra" : 10.0,
                                            "categoria" : "Alimentos"
                                        },
							"importe": 80
					    },
                        {
                            "cantidad": 3, 
							"impuestos": 0.16,
							"descuento_producto": 0.00,
							"producto": 	{
                                                "_id" : "3",
                                                "nombre" : "Café",
                                                "precio_venta" : 25,
                                                "precio_compra" : 10,
                                                "categoria" : "Bebidas"
                                            },
							"importe": 50
                        }
					   ]
    },
    {
		"_id": "5",
		"total": 80.0,
        "descuento": 20.0, #porcentaje
		"fecha": "2020-07-06T10:00:00Z",
		"id_participante": "5e599aacf97a00a6036b17b0",
		# forma_pago: {
		# 			nombre: "efectivo", 
		# 			otros_detalles: "Datos de la terminal importantes"
		# 			},
		# qr: "asdaqwke923jl4jql0jqeqeq",
		# descuento_general: 15.5,
		# usuario_id_usuario: usuario__id,
        "promociones": [3,4],
		"detalle_venta": [
						{
							"cantidad": 1, 
							"impuestos": 0.16,
							"descuento_producto": 0.00,
							"producto": 	{
                                            "_id" : "2",
                                            "nombre" : "Bolipán",
                                            "precio_venta" : 20.0,
                                            "precio_compra" : 10.0,
                                            "categoria" : "Alimentos"
                                        },
							"importe": 80
					    },
                        {
                            "cantidad": 3, 
							"impuestos": 0.16,
							"descuento_producto": 0.00,
							"producto": 	{
                                                "_id" : "3",
                                                "nombre" : "Café",
                                                "precio_venta" : 25,
                                                "precio_compra" : 10,
                                                "categoria" : "Bebidas"
                                            },
							"importe": 50
                        }
					   ]
    },
    {
		"_id": "6",
		"total": 80.0,
        "descuento": 20.0, #porcentaje
		"fecha": "2020-08-06T10:00:00Z",
		"id_participante": "5e599aacf97a00a6036b17b1",
		# forma_pago: {
		# 			nombre: "efectivo", 
		# 			otros_detalles: "Datos de la terminal importantes"
		# 			},
		# qr: "asdaqwke923jl4jql0jqeqeq",
		# descuento_general: 15.5,
		# usuario_id_usuario: usuario__id,
        "promociones": [3,4],
		"detalle_venta": [
						{
							"cantidad": 1, 
							"impuestos": 0.16,
							"descuento_producto": 0.00,
							"producto": 	{
                                            "_id" : "2",
                                            "nombre" : "Bolipán",
                                            "precio_venta" : 20.0,
                                            "precio_compra" : 10.0,
                                            "categoria" : "Alimentos"
                                        },
							"importe": 80
					    },
                        {
                            "cantidad": 3, 
							"impuestos": 0.16,
							"descuento_producto": 0.00,
							"producto": 	{
                                                "_id" : "3",
                                                "nombre" : "Café",
                                                "precio_venta" : 25,
                                                "precio_compra" : 10,
                                                "categoria" : "Bebidas"
                                            },
							"importe": 50
                        }
					   ]
    },
    {
		"_id": "7",
		"total": 80.0,
        "descuento": 20.0, #porcentaje
		"fecha": "2020-09-06T10:00:00Z",
		"id_participante": "5e599aacf97a00a6036b17b2",
		# forma_pago: {
		# 			nombre: "efectivo", 
		# 			otros_detalles: "Datos de la terminal importantes"
		# 			},
		# qr: "asdaqwke923jl4jql0jqeqeq",
		# descuento_general: 15.5,
		# usuario_id_usuario: usuario__id,
        "promociones": [3,4],
		"detalle_venta": [
						{
							"cantidad": 1, 
							"impuestos": 0.16,
							"descuento_producto": 0.00,
							"producto": 	{
                                            "_id" : "2",
                                            "nombre" : "Bolipán",
                                            "precio_venta" : 20.0,
                                            "precio_compra" : 10.0,
                                            "categoria" : "Alimentos"
                                        },
							"importe": 80
					    },
                        {
                            "cantidad": 3, 
							"impuestos": 0.16,
							"descuento_producto": 0.00,
							"producto": 	{
                                                "_id" : "3",
                                                "nombre" : "Café",
                                                "precio_venta" : 25,
                                                "precio_compra" : 10,
                                                "categoria" : "Bebidas"
                                            },
							"importe": 50
                        }
					   ]
    },
    {
		"_id": "8",
		"total": 80.0,
        "descuento": 20.0, #porcentaje
		"fecha": "2020-10-06T10:00:00Z",
		"id_participante": "5e599aacf97a00a6036b17b3",
		# forma_pago: {
		# 			nombre: "efectivo", 
		# 			otros_detalles: "Datos de la terminal importantes"
		# 			},
		# qr: "asdaqwke923jl4jql0jqeqeq",
		# descuento_general: 15.5,
		# usuario_id_usuario: usuario__id,
        "promociones": [3,4],
		"detalle_venta": [
						{
							"cantidad": 1, 
							"impuestos": 0.16,
							"descuento_producto": 0.00,
							"producto": 	{
                                            "_id" : "2",
                                            "nombre" : "Bolipán",
                                            "precio_venta" : 20.0,
                                            "precio_compra" : 10.0,
                                            "categoria" : "Alimentos"
                                        },
							"importe": 80
					    },
                        {
                            "cantidad": 3, 
							"impuestos": 0.16,
							"descuento_producto": 0.00,
							"producto": 	{
                                                "_id" : "3",
                                                "nombre" : "Café",
                                                "precio_venta" : 25,
                                                "precio_compra" : 10,
                                                "categoria" : "Bebidas"
                                            },
							"importe": 50
                        }
					   ]
    }
]




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
    def get(self):
        req = request.get_json()
        filtersList = []
        try:
            for fi in req:
                idList = []
                if fi['document'] == 'participante_model_tarjeta_sellos':     
                    if fi['method'] == 'filter_by_date_range':
                        fi = TarjetaSellosModel.filter_by_date_range(fi['date_start'], fi['date_end'], fi['field'])
                    elif fi['method'] == 'filter_by_date':
                        fi = TarjetaSellosModel.filter_by_date(fi['date_start'], fi['tipo'], fi['scale'], fi['scale_value'], fi['field'])
                    elif fi['method'] == 'filter_by_float_range':
                        fi = TarjetaSellosModel.filter_by_float_range(fi['tipo'], fi['field'], fi['float1'], fi['float2'])
                    elif fi['method'] == 'filter_by_float':
                        fi = TarjetaSellosModel.filter_by_float(fi['tipo'], fi['float1'], fi['field'])
                    elif fi['method'] == 'filter_by_integer_range':
                        fi = TarjetaSellosModel.filter_by_integer_range(fi['tipo'], fi['field'], fi['int1'], fi['int2'])
                    elif fi['method'] == 'filter_by_integer':
                        fi = TarjetaSellosModel.filter_by_integer(fi['tipo'], fi['int1'], fi['field'])
                    elif fi['method'] == 'filter_by_string':
                        fi = TarjetaSellosModel.filter_by_string(fi['field'],fi['tipo'], fi['str1'])
                    if type(fi) == tuple:
                        filtersList.append( fi )
                    elif fi:
                        # Hardcoded Match relationship between two collections
                        encuestas = list(fi.only("_id").values())
                        # print("\n\n", encuestas)
                        encuesta_ids_list = []
                        for e in encuestas:
                            encuesta_ids_list.append({'tarjeta_sellos' : e['_id']})
                        if encuestas:
                            fi = ParticipanteModel.objects.raw({ "$or" : encuesta_ids_list})
                        # print(list(fi))
                        cursor  = fi.aggregate(
                            {'$group': {'_id': '$_id'}},
                            allowDiskUse=True)
                        cursorList = list(cursor)
                        for item in cursorList:
                                idList.append(str(item['_id']))
                    filtersList.append({
                        "participantes" : idList,
                        "total": len(idList),
                    })
                elif fi['document'] == 'participante_model_tarjeta_puntos':     
                    if fi['method'] == 'filter_by_date_range':
                        fi = TarjetaPuntosModel.filter_by_date_range(fi['date_start'], fi['date_end'], fi['field'])
                    elif fi['method'] == 'filter_by_date':
                        fi = TarjetaPuntosModel.filter_by_date(fi['date_start'], fi['tipo'], fi['scale'], fi['scale_value'], fi['field'])
                    elif fi['method'] == 'filter_by_float_range':
                        fi = TarjetaPuntosModel.filter_by_float_range(fi['tipo'], fi['field'], fi['float1'], fi['float2'])
                    elif fi['method'] == 'filter_by_float':
                        fi = TarjetaPuntosModel.filter_by_float(fi['tipo'], fi['float1'], fi['field'])
                    elif fi['method'] == 'filter_by_integer_range':
                        fi = TarjetaPuntosModel.filter_by_integer_range(fi['tipo'], fi['field'], fi['int1'], fi['int2'])
                    elif fi['method'] == 'filter_by_integer':
                        fi = TarjetaPuntosModel.filter_by_integer(fi['tipo'], fi['int1'], fi['field'])
                    elif fi['method'] == 'filter_by_string':
                        fi = TarjetaPuntosModel.filter_by_string(fi['field'],fi['tipo'], fi['str1'])
                    if type(fi) == tuple:
                        filtersList.append( fi )
                    elif fi:
                        # Hardcoded Match relationship between two collections
                        encuestas = list(fi.only("_id").values())
                        # print("\n\n", encuestas)
                        encuesta_ids_list = []
                        for e in encuestas:
                            encuesta_ids_list.append({'tarjeta_puntos' : e['_id']})
                        if encuestas:
                            fi = ParticipanteModel.objects.raw({ "$or" : encuesta_ids_list})
                        # print(list(fi))
                        cursor  = fi.aggregate(
                            {'$group': {'_id': '$_id'}},
                            allowDiskUse=True)
                        cursorList = list(cursor)
                        for item in cursorList:
                                idList.append(str(item['_id']))
                    filtersList.append({
                        "participantes" : idList,
                        "total": len(idList),
                    })
                elif fi['document'] == 'participante_model':     
                    if fi['method'] == 'filter_by_date_range':
                        fi = ParticipanteModel.filter_by_date_range(fi['date_start'], fi['date_end'], fi['field'])
                    elif fi['method'] == 'filter_by_date':
                        fi = ParticipanteModel.filter_by_date(fi['date_start'], fi['tipo'], fi['scale'], fi['scale_value'], fi['field'])
                    elif fi['method'] == 'filter_by_float_range':
                        fi = ParticipanteModel.filter_by_float_range(fi['tipo'], fi['field'], fi['float1'], fi['float2'])
                    elif fi['method'] == 'filter_by_float':
                        fi = ParticipanteModel.filter_by_float(fi['tipo'], fi['float1'], fi['field'])
                    elif fi['method'] == 'filter_by_integer_range':
                        fi = ParticipanteModel.filter_by_integer_range(fi['tipo'], fi['field'], fi['int1'], fi['int2'])
                    elif fi['method'] == 'filter_by_integer':
                        fi = ParticipanteModel.filter_by_integer(fi['tipo'], fi['int1'], fi['field'])
                    elif fi['method'] == 'filter_by_string':
                        fi = ParticipanteModel.filter_by_string(fi['field'],fi['tipo'], fi['str1'])
                    if type(fi) == tuple:
                        filtersList.append( fi )
                    elif fi:
                        for p in fi:
                            idList.append(str(p._id))
                    filtersList.append(  {
                        "participantes" : idList,
                        "total": len(idList),
                    })
                elif fi['document'] == 'participante_premio_model':  
                    if fi['method'] == 'filter_by_date_range':
                        fi = PremioParticipanteModel.filter_by_date_range(fi['date_start'], fi['date_end'], fi['field'])
                    elif fi['method'] == 'filter_by_date':
                        fi = PremioParticipanteModel.filter_by_date(fi['date_start'], fi['tipo'], fi['scale'], fi['scale_value'], fi['field'])
                    elif fi['method'] == 'filter_by_float_range':
                        fi = PremioParticipanteModel.filter_by_float_range(fi['tipo'], fi['field'], fi['float1'], fi['float2'])
                    elif fi['method'] == 'filter_by_float':
                        fi = PremioParticipanteModel.filter_by_float(fi['tipo'], fi['float1'], fi['field'])
                    elif fi['method'] == 'filter_by_integer_range':
                        fi = PremioParticipanteModel.filter_by_integer_range(fi['tipo'], fi['field'], fi['int1'], fi['int2'])
                    elif fi['method'] == 'filter_by_integer':
                        fi = PremioParticipanteModel.filter_by_integer(fi['tipo'], fi['int1'], fi['field'])
                    elif fi['method'] == 'filter_by_string':
                        fi = PremioParticipanteModel.filter_by_string(fi['field'],fi['tipo'], fi['str1'])
                    elif fi['method'] == 'filter_by_date_range_in_array':
                        fi = PremioParticipanteModel.filter_by_date_range_in_array(fi['date_start'], fi['date_end'], fi['field'])
                    elif fi['method'] == 'filter_by_date_in_array':
                        fi = PremioParticipanteModel.filter_by_date_in_array(fi['date_start'], fi['tipo'], fi['scale'], fi['scale_value'], fi['field'])
                    elif fi['method'] == 'filter_by_float_in_array':
                        fi = PremioParticipanteModel.filter_by_float_in_array(fi['tipo'], fi['float1'], fi['field'])
                    elif fi['method'] == 'filter_by_integer_range_in_array':
                        fi = PremioParticipanteModel.filter_by_integer_range_in_array(fi['tipo'], fi['field'], fi['int1'], fi['int2'])
                    elif fi['method'] == 'filter_by_integer_in_array':
                        fi = PremioParticipanteModel.filter_by_integer_in_array(fi['tipo'], fi['int1'], fi['field'])
                    elif fi['method'] == 'filter_by_string_in_array':
                        fi = PremioParticipanteModel.filter_by_string_in_array(fi['field'],fi['tipo'], fi['str1'])
                    elif fi['method'] == 'filter_by_elements_range_in_array':
                        fi = PremioParticipanteModel.filter_by_elements_range_in_array(fi['tipo'], fi['field'], fi['int1'], fi['int2'])
                    elif fi['method'] == 'filter_by_elements_in_array':
                        fi = PremioParticipanteModel.filter_by_elements_in_array(fi['tipo'], fi['int1'], fi['field'])
                    elif fi['method'] == 'filter_by_elements_in_array':
                        fi = PremioParticipanteModel.filter_by_elements_in_array(fi['tipo'], fi['int1'], fi['field'])
                    if type(fi) == tuple:
                        filtersList.append( fi )
                    elif fi:
                        cursor  = fi.aggregate(
                            {'$group': {'_id': '$id_participante'}},
                            allowDiskUse=True)
                        cursorList = list(cursor)
                        for item in cursorList:
                                idList.append(str(item['_id']))
                    filtersList.append({
                        "participantes" : idList,
                        "total": len(idList),
                    })
                elif fi['document'] == 'venta_model':  
                    if fi['method'] == 'filter_by_date_range':
                        fi = VentaModel.filter_by_date_range(fi['date_start'], fi['date_end'], fi['field'])
                    elif fi['method'] == 'filter_by_date':
                        fi = VentaModel.filter_by_date(fi['date_start'], fi['tipo'], fi['scale'], fi['scale_value'], fi['field'])
                    elif fi['method'] == 'filter_by_float_range':
                        fi = VentaModel.filter_by_float_range(fi['tipo'], fi['field'], fi['float1'], fi['float2'])
                    elif fi['method'] == 'filter_by_float':
                        fi = VentaModel.filter_by_float(fi['tipo'], fi['float1'], fi['field'])
                    elif fi['method'] == 'filter_by_integer_range':
                        fi = VentaModel.filter_by_integer_range(fi['tipo'], fi['field'], fi['int1'], fi['int2'])
                    elif fi['method'] == 'filter_by_integer':
                        fi = VentaModel.filter_by_integer(fi['tipo'], fi['int1'], fi['field'])
                    elif fi['method'] == 'filter_by_string':
                        fi = VentaModel.filter_by_string(fi['field'],fi['tipo'], fi['str1'])
                    if type(fi) == tuple:
                        filtersList.append( fi )
                    elif fi:
                        cursor  = fi.aggregate(
                            {'$group': {'_id': '$id_participante'}},
                            allowDiskUse=True)
                        cursorList = list(cursor)
                        for item in cursorList:
                                idList.append(str(item['_id']))
                    filtersList.append({
                        "participantes" : idList,
                        "total": len(idList),
                    })
                elif fi['document'] == 'encuesta_model':  
                    if fi['method'] == 'filter_by_date_range':
                        fi = EncuestaModel.filter_by_date_range(fi['date_start'], fi['date_end'], fi['field'])
                    elif fi['method'] == 'filter_by_date':
                        fi = EncuestaModel.filter_by_date(fi['date_start'], fi['tipo'], fi['scale'], fi['scale_value'], fi['field'])
                    elif fi['method'] == 'filter_by_float_range':
                        fi = EncuestaModel.filter_by_float_range(fi['tipo'], fi['field'], fi['float1'], fi['float2'])
                    elif fi['method'] == 'filter_by_float':
                        fi = EncuestaModel.filter_by_float(fi['tipo'], fi['float1'], fi['field'])
                    elif fi['method'] == 'filter_by_integer_range':
                        fi = EncuestaModel.filter_by_integer_range(fi['tipo'], fi['field'], fi['int1'], fi['int2'])
                    elif fi['method'] == 'filter_by_integer':
                        fi = EncuestaModel.filter_by_integer(fi['tipo'], fi['int1'], fi['field'])
                    elif fi['method'] == 'filter_by_string':
                        fi = EncuestaModel.filter_by_string(fi['field'],fi['tipo'], fi['str1'])
                    elif fi['method'] == 'filter_by_date_range_in_array':
                        fi = EncuestaModel.filter_by_date_range_in_array(fi['date_start'], fi['date_end'], fi['field'])
                    elif fi['method'] == 'filter_by_date_in_array':
                        fi = EncuestaModel.filter_by_date_in_array(fi['date_start'], fi['tipo'], fi['scale'], fi['scale_value'], fi['field'])
                    elif fi['method'] == 'filter_by_float_in_array':
                        fi = EncuestaModel.filter_by_float_in_array(fi['tipo'], fi['float1'], fi['field'])
                    elif fi['method'] == 'filter_by_integer_range_in_array':
                        fi = EncuestaModel.filter_by_integer_range_in_array(fi['tipo'], fi['field'], fi['int1'], fi['int2'])
                    elif fi['method'] == 'filter_by_integer_in_array':
                        fi = EncuestaModel.filter_by_integer_in_array(fi['tipo'], fi['int1'], fi['field'])
                    elif fi['method'] == 'filter_by_string_in_array':
                        fi = EncuestaModel.filter_by_string_in_array(fi['field'],fi['tipo'], fi['str1'])
                    elif fi['method'] == 'filter_by_elements_range_in_array':
                        fi = EncuestaModel.filter_by_elements_range_in_array(fi['tipo'], fi['field'], fi['int1'], fi['int2'])
                    elif fi['method'] == 'filter_by_elements_in_array':
                        fi = EncuestaModel.filter_by_elements_in_array(fi['tipo'], fi['int1'], fi['field'])
                    elif fi['method'] == 'filter_by_elements_in_array':
                        fi = EncuestaModel.filter_by_elements_in_array(fi['tipo'], fi['int1'], fi['field'])
                    if type(fi) == tuple:
                        filtersList.append( fi )
                    elif fi:
                        # Hardcoded Match relationship between two collections
                        # print(list(fi))
                        encuestas = fi.only("_id").values()
                        # print(list(encuestas))
                        encuesta_ids_list = []
                        for e in encuestas:
                            encuesta_ids_list.append({'id_encuesta' : str(e['_id'])})
                        # print(encuesta_ids_list)
                        # print("len:",len(encuesta_ids_list))
                        if len(encuesta_ids_list):
                            fi = ParticipantesEncuestaModel.objects.raw({ "$or" : encuesta_ids_list})
                        cursor  = fi.aggregate(
                            {'$group': {'_id': '$id_participante'}},
                            allowDiskUse=True)
                        cursorList = list(cursor)
                        for item in cursorList:
                                idList.append(str(item['_id']))
                    filtersList.append({
                        "participantes" : idList,
                        "total": len(idList),
                    })
                elif fi['document'] == 'participantes_encuesta_model':  
                    if fi['method'] == 'filter_by_date_range':
                        fi = ParticipantesEncuestaModel.filter_by_date_range(fi['date_start'], fi['date_end'], fi['field'])
                    elif fi['method'] == 'filter_by_date':
                        fi = ParticipantesEncuestaModel.filter_by_date(fi['date_start'], fi['tipo'], fi['scale'], fi['scale_value'], fi['field'])
                    elif fi['method'] == 'filter_by_float_range':
                        fi = ParticipantesEncuestaModel.filter_by_float_range(fi['tipo'], fi['field'], fi['float1'], fi['float2'])
                    elif fi['method'] == 'filter_by_float':
                        fi = ParticipantesEncuestaModel.filter_by_float(fi['tipo'], fi['float1'], fi['field'])
                    elif fi['method'] == 'filter_by_integer_range':
                        fi = ParticipantesEncuestaModel.filter_by_integer_range(fi['tipo'], fi['field'], fi['int1'], fi['int2'])
                    elif fi['method'] == 'filter_by_integer':
                        fi = ParticipantesEncuestaModel.filter_by_integer(fi['tipo'], fi['int1'], fi['field'])
                    elif fi['method'] == 'filter_by_string':
                        fi = ParticipantesEncuestaModel.filter_by_string(fi['field'],fi['tipo'], fi['str1'])
                    elif fi['method'] == 'filter_by_date_range_in_array':
                        fi = ParticipantesEncuestaModel.filter_by_date_range_in_array(fi['date_start'], fi['date_end'], fi['field'])
                    elif fi['method'] == 'filter_by_date_in_array':
                        fi = ParticipantesEncuestaModel.filter_by_date_in_array(fi['date_start'], fi['tipo'], fi['scale'], fi['scale_value'], fi['field'])
                    elif fi['method'] == 'filter_by_float_in_array':
                        fi = ParticipantesEncuestaModel.filter_by_float_in_array(fi['tipo'], fi['float1'], fi['field'])
                    elif fi['method'] == 'filter_by_integer_range_in_array':
                        fi = ParticipantesEncuestaModel.filter_by_integer_range_in_array(fi['tipo'], fi['field'], fi['int1'], fi['int2'])
                    elif fi['method'] == 'filter_by_integer_in_array':
                        fi = ParticipantesEncuestaModel.filter_by_integer_in_array(fi['tipo'], fi['int1'], fi['field'])
                    # elif fi['method'] == 'filter_by_string_in_array':
                    #     fi = ParticipantesEncuestaModel.filter_by_string_in_array(fi['field'],fi['tipo'], fi['str1'])
                    elif fi['method'] == 'filter_by_elements_range_in_array':
                        fi = ParticipantesEncuestaModel.filter_by_elements_range_in_array(fi['tipo'], fi['field'], fi['int1'], fi['int2'])
                    elif fi['method'] == 'filter_by_elements_in_array':
                        fi = ParticipantesEncuestaModel.filter_by_elements_in_array(fi['tipo'], fi['int1'], fi['field'])
                    elif fi['method'] == 'filter_by_elements_in_array':
                        fi = ParticipantesEncuestaModel.filter_by_elements_in_array(fi['tipo'], fi['int1'], fi['field'])
                    if type(fi) == tuple:
                        filtersList.append( fi )
                    elif fi:
                        cursor  = fi.aggregate(
                            {'$group': {'_id': '$id_participante'}},
                            allowDiskUse=True)
                        cursorList = list(cursor)
                        for item in cursorList:
                                idList.append(str(item['_id']))
                    filtersList.append({
                        "participantes" : idList,
                        "total": len(idList),
                    })
            return  filtersList, 200
                # elif fi['document'] == 'encuesta_model':                             
        except ParticipanteModel.DoesNotExist:
            return {'message': 'Ocurrió un error al procesar su petición'}, 500
        # # Número de participantes nuevos
        # if idMetrica == '1': 
        #     try:
        #         if 'date_end' in req:
        #             participantes_nuevos = ParticipanteModel.filter_by_date_range(req['date_start'], req['date_end'], req['field'])
        #         else:
        #             participantes_nuevos = ParticipanteModel.filter_by_date(req['date_start'], req['tipo'], req['scale'], req['scale_value'], req['field'])
        #         # TODO: Si es necesario más tarde, Este bloque evita que se cometan errores sintacticos en las solicitudes
        #         # if not participantes_nuevos:
        #         #     return {"message": "Revise los parametros en la solicitud: Alguno(s) de los campos enviados en el formulario y/o su respectivo valor tienen un error sintáctico o no existen participantes con esos atributos en la base de datos"}, 404
        #         if participantes_nuevos:
        #             for p in participantes_nuevos:
        #                 idList.append(str(p._id))
        #         return {
        #             "participantes" : idList,
        #             "total": len(idList),
        #             }, 200
        #     except ParticipanteModel.DoesNotExist:
        #         return {'message': 'Ocurrió un error al procesar su petición'}, 500
        # # Numero de premios entregados
        # elif idMetrica == '2': 
        #     try:
        #         if 'date_end' in req:
        #             premios_entregados = PremioParticipanteModel.filter_by_date_range(req['date_start'], req['date_end'], req['field'])
        #         else:
        #             premios_entregados = PremioParticipanteModel.filter_by_date(req['date_start'], req['tipo'], req['scale'], req['scale_value'], req['field'])
        #             cursor  = premios_entregados.aggregate(
        #                 {'$group': {'_id': '$id_participante', 'count': {'$sum': 1}}},
        #                 {'$sort': {'price': pymongo.DESCENDING}},
        #                 allowDiskUse=True)
        #             # print(list(cursor))
        #             a = list(cursor)
        #             print(a, "---", len(a), len(list(premios_entregados)))
        #         if premios_entregados:
        #             for p in a:
        #                 # pprint("ele#mnt")
        #                 idList.append({ '_id' : str(p['_id']), 'count' : p['count']})
        #         # print(idList)
        #         return {
        #             "premios_entregados" : idList,
        #             "total": len(list(premios_entregados)
        #             )   
        #         }
        #         # {
        #         #     "participantes" : idList,
        #         #     "total": len(idList),
        #         #     }, 200
        #     except ParticipanteModel.DoesNotExist:
        #         return {'message': 'Ocurrió un error al procesar su petición'}, 500
        return {'message': 'Valor: IdMetrica invalido'}, 400
            