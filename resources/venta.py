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


from models.premio import PremioModel, PremioParticipanteModel
from models.participante import ParticipanteModel
from models.producto import CatalogoModel

from schemas.premio import PremioSchema, PremioParticipanteSchema
from schemas.participante import ParticipanteSchema 
from schemas.producto import CatalogoSchema
from marshmallow import pprint

participante_schema = ParticipanteSchema()

productos = [
    {
        "_id" : "1",
        "nombre" : "bubbleTea",
        "precio" : 55,
        "costo" : 30,
        "categoria" : "Bebidas"
    },
    {
        "_id" : "2",
        "nombre" : "Bolipán",
        "precio" : 20,
        "costo" : 10,
        "categoria" : "Alimentos"
    },
    {
        "_id" : "3",
        "nombre" : "Café",
        "precio" : 25,
        "costo" : 10,
        "categoria" : "Bebidas"
    }
]

# Si se canjea una promo no se obtiene reward points! 
# La diferencia entre una promoción y un premio al realizar una compra
#  es que en la : 
# `Promoción` se obtiene un beneficio económico, en producto o en puntos  y
#  en el `Premio` el único beneficio es puntos que en un futuro desbloquearán un
#  Premio, en otras palabras los premios NO EXISTEN hasta que se desbloquean gracias
#  a las promociones que acumularon el conteo de Puntos
#  Una promoción también puede otorgar sellos!
# :::> Promoción debería llamarse Recompensas

#  NOTE: Si fecha_vigencia es "" o null entonces no tiene vigencia
#  NOTE: Promocion :
#        te llevas estos productos:         a el precio de:
#         [P1, P2, ..., Pn]                   [P1, P2, ... , Pn ]
#               donde P es un producto
#       Considera que un combo es posible, primero: creando un producto que haga
#       referencia a este combo y tenga el precio que tendrá el combo y segundo:
#       asignar una promocion con n productos por el precio de este producto "promoción X"
#       que acabas de crear
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
        # Ejemplo de la estructura en la siguiente version! v/2
#    {
# 		"_id": "1",
# 		"titulo": "50% de descuento en la compra de un frappé Halloween",
# 		"tipo": "porcentaje",
# 		"valor": 50.0,
#         "productos_requeridos": [
#             "categorias": [
#                 {
#                     "id_categoria":"1", 
#                     "cantidad": 1.0, 
#                     "descuento": 20.0
#                 }
#             ], 
#             "productos": [
#                 {
#                     "id_producto":"1", 
#                     "cantidad": 1.0, 
#                     "descuento": 20.0
#                 }
#             ] #descuento: porcentaje %
#         ], #Productos que se requieren para cumplir la promoción
#         "productos_oferta":[
#             {
#                 "id_producto":"2",
#                 "descuento": 50.0
#             },
#             {"producto":"2","descuento": 50.0}]
# 		"fecha_vigencia":  "2021-06-06T16:00:00Z",
#         "puntos": 0.0,
#         "sellos": 0
# 	},
    # # Compra una X y llevate la segunda al 50 %
    # {
	# 	"_id": "3",
	# 	"titulo": "Compra un bolipán y llevate el segundo a la mitad de precio",
	# 	"tipo": "combo",
	# 	"valor": 0.0, # No importa
    #     "productos_requeridos": [  #Productos que se requieren para cumplir la promoción
    #         # "categorias": [
    #         #     {
    #         #         "id_categoria":"1", 
    #         #         "cantidad": 1.0, 
    #         #         "descuento": 20.0
    #         #     }
    #         # ], 
    #         "productos": [
    #             {
    #                 "id_producto":"2", 
    #                 "cantidad": 2.0, 
    #                 "descuento": 20.0
    #             }
    #         ] #descuento: porcentaje %
    #     ], 
    #     "productos_oferta":[
    #         {
    #             "id_producto":"2",
    #             "descuento": 0.0
    #         }
    #         {
    #             "id_producto":"2",
    #             "descuento": 50.0
    #         }            
	# 	"fecha_vigencia":  "2021-06-06T16:00:00Z",
    #     "puntos": 0.0,
    #     "sellos": 0
	# },
]

tickets = [
    {
		"_id": "1",
		"total": 80.00,
        "descuento": 20.0, #porcentaje
		"fecha": "2020-06-06T10:00:00Z",
		"id_participante": "5e462b2f174d02be8e6fabb0",
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
                                            "precio" : 20.0,
                                            "costo" : 10.0,
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
                                            "precio" : 55.0,
                                            "costo" : 30.0,
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
		"id_participante": "5e462b2f174d02be8e6fabb0",
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
                                            "precio" : 20.0,
                                            "costo" : 10.0,
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
		"id_participante": "5e462b2f174d02be8e6fabb0",
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
                                            "precio" : 20.0,
                                            "costo" : 10.0,
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
                                                "precio" : 25,
                                                "costo" : 10,
                                                "categoria" : "Bebidas"
                                            },
							"importe": 50
                        }
					   ]
    }
]


class ProductoList(Resource):
    @classmethod
    def get(self):
        # reques = request.get_json()
        # if "hola" in reques:
        #     print(reques['hola'], type(reques['hola']))
        return productos, 200


class Producto(Resource):
    @classmethod
    def get(self, id):
        for index, item in enumerate(productos):
            print(item)
            if(item['_id'] ==  id):
                return item, 200
        return {'No existe un producto con ese _id'}, 404
        


class PromocionList(Resource):
    @classmethod
    def get(self): 
        return promociones, 200


class Promocion(Resource):
    @classmethod
    def get(self, id):
        for index, item in enumerate(promociones):
            print(item)
            if(item['_id'] ==  id):
                return item, 200
        return {'No existe una promocion con ese _id'}, 404


class TicketList(Resource):
    @classmethod
    def get(self):
        return tickets, 200

class Ticket(Resource):
    @classmethod
    def get(self, id):
        for index, item in enumerate(tickets):
            print(item)
            if(item['_id'] ==  id):
                return item, 200
        return {'No existe un ticket con ese _id'}, 404