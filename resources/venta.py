import json
import datetime as dt
import functools
import uuid 
from bson.objectid import ObjectId

from flask import request, jsonify
from flask_restful import Resource

from models.producto import *
from models.venta import *
from models.empleado import *
from models.promocion import *

from schemas.venta import *

from pymodm.errors import ValidationError
from pymongo.errors import DuplicateKeyError
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
		"_id": '5e701fba1377db6386eb11da',
		"titulo": "BubbleCombo",
        "descripcion": "por la compra de un blbla..",
        # "imagen": "https://bubbletown.com/download/promo1.png", 
        "imagen": "http://127.0.0.1:5001/download/promo1.png", 
		"precio_venta": 100.0,
        "costo_venta": 50.0,
		"fecha_vigencia_start":  "2029-06-06T16:00:00Z",
		"fecha_vigencia_end":  "2029-06-06T16:00:00Z",
	},
    {
		"_id": '5e701fba1377db6386eb11da',
		"titulo": "50% de descuento sobre tu compra",
        "descripcion": "por la compra de un...",
        # "imagen": "https://bubbletown.com/download/promo2.png", 
        "imagen": "http://127.0.0.1:5001/download/promo2.png", 
		"precio_venta": 100.0,
        "costo_venta": 50.0,
		"fecha_vigencia_start":  "2029-06-06T16:00:00Z",
		"fecha_vigencia_end":  "2029-06-06T16:00:00Z",
	},
    {
		"_id": '5e701fba1377db6386eb11da',
		"titulo": "2x1 en bolipanes",
        "descripcion": "por la compra de un...",
        # "imagen": "https://bubbletown.com/download/promo3.png", 
        "imagen": "http://127.0.0.1:5001/download/promo3.png", 
		"precio_venta": 100.0,
        "costo_venta": 50.0,
		"fecha_vigencia_start":  "2029-06-06T16:00:00Z",
		"fecha_vigencia_end":  "2029-06-06T16:00:00Z",
	},
    {
		"_id": '5e701fba1377db6386eb11da',
		"titulo": "3x2 en café",
        "descripcion": "por la compra de un...",
        # "imagen": "https://bubbletown.com/download/promo3.png", 
        "imagen": "http://127.0.0.1:5001/download/promo3.png", 
		"precio_venta": 100.0,
        "costo_venta": 50.0,
		"fecha_vigencia_start":  "2029-06-06T16:00:00Z",
		"fecha_vigencia_end":  "2029-06-06T16:00:00Z",
	},
    {
		"_id": '5e701fba1377db6386eb11da',
		"titulo": "Combo: 3 bolipanes + 1 bubbleFreezze mediano por $179",
        "descripcion": "por la compra de un...",
        "imagen": "http://127.0.0.1:5001/download/promo4.jpg", 
		"precio_venta": 100.0,
        "costo_venta": 50.0,
		"fecha_vigencia_start":  "2029-06-06T16:00:00Z",
		"fecha_vigencia_end":  "2029-06-06T16:00:00Z",
	}
	# {
	# 	"_id": "5e701fc31377db6386eb11d",
	# 	"titulo": "50% de descuento sobre tu compra",
	# 	"tipo": "porcentaje compra",
	# 	"valor": 50.0,
	# 	"productos_validos": ["5e701e771377db6386eb11d5","5e701e951377db6386eb11d7"],
	# 	"fecha_vigencia":  "2020-06-06T16:00:00Z",
    #     "puntos": 0.0,
    #     "sellos": 0
	# },
    # {
	# 	"_id": "5e701fd11377db6386eb11dc",
	# 	"titulo": "2x1 en bolipanes",
	# 	"tipo": "2", 
	# 	"valor": 1.0,  
	# 	"productos_validos": ["5e701e8c1377db6386eb11d6"],
	# 	"fecha_vigencia":  "2020-06-06T16:00:00Z",
    #     "puntos": 0.0,
    #     "sellos": 0
	# },
    # {
	# 	"_id": "5e701fe11377db6386eb11dd",
	# 	"titulo": "3x2 en café",
	# 	"tipo": "3", 
	# 	"valor": 2.0, 
	# 	"productos_validos": ["5e701e951377db6386eb11d7"],
	# 	"fecha_vigencia":  "2020-06-06T16:00:00Z",
    #     "puntos": 0.0,
    #     "sellos": 0
	# },
    # {
	# 	"_id": "5e701fe11377db6386eb11dd",
	# 	"titulo": "Combo",
	# 	"tipo": "3", 
	# 	"valor": 2.0, 
	# 	"productos_validos": ["5e701e951377db6386eb11d7"],
	# 	"fecha_vigencia":  "2020-06-06T16:00:00Z",
    #     "puntos": 0.0,
    #     "sellos": 0
	# }
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

# ticket = {
#     "_id": "1",
#     "total_pesos": 80.00,
#     "descuento_pesos": 20.0,
#     "fecha": "2020-06-06T10:00:00Z",
#     "id_participante": "5e462b2f174d02be8e6fabb0",
#     "promociones": ["5e701fba1377db6386eb11da", "5e701fc31377db6386eb11db"],
#     "detalle_venta": [
#         {
#             "cantidad": 2, 
#             "descuento_pesos": 50.0,
#             "producto": 	{
#                             "_id" : "5e701e8c1377db6386eb11d6",
#                             "nombre" : "Bolipán",
#                             "precio_venta" : 20.0,
#                             "precio_compra" : 10.0,
#                             "categoria" : "Alimentos"
#                         },
#             "importe": 20
#         },
#         {
#             "cantidad": 2, 
#             "descuento_pesos": 55.00,
#             "producto": 	
#                         {
#                             "_id" : "5e701e771377db6386eb11d5",
#                             "nombre" : "bubbleTea",
#                             "precio_venta" : 55.0,
#                             "precio_compra" : 30.0,
#                             "categoria" : "Bebidas"
#                         },
#             "importe": 55.0
#         }
#     ]
# }

tickets = [
    {
		"_id": "1",
		"total_pesos": 80.00,
        "descuento_pesos": 20.0,
		"fecha": "2020-06-06T10:00:00Z",
		"id_participante": "5e462b2f174d02be8e6fabb0",
        "promociones": ["5e701fba1377db6386eb11da", "5e701fc31377db6386eb11db"],
		"detalle_venta": [
						{
							"cantidad": 2, 
							"descuento_pesos": 50.0,
							"producto": 	{
                                            "_id" : "5e701e8c1377db6386eb11d6",
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
                                            "_id" : "5e701e771377db6386eb11d5",
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
		"fecha": "2022-06-06T10:00:00Z",
		"id_participante": "5e462b2f174d02be8e6fabb0",
        "promociones": [],
		"detalle_venta": [
						{
							"cantidad": 1, 
							"impuestos": 0.16,
							"descuento_producto": 0.00,
							"producto": 	{
                                            "_id" : "5e701e8c1377db6386eb11d6",
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
		"fecha": "2021-10-06T10:00:00Z",
		"id_participante": "5e6f6e1a210261e9f3c2b15d",
        "promociones": ["5e701fd11377db6386eb11dc", "5e701fe11377db6386eb11dd"],
		"detalle_venta": [
						{
							"cantidad": 1, 
							"impuestos": 0.16,
							"descuento_producto": 0.00,
							"producto": 	{
                                            "_id" : "5e701e8c1377db6386eb11d6",
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
                                                "_id" : "5e701e951377db6386eb11d7",
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


class ProductoList(Resource):
    @classmethod
    def get(self):
        # reques = request.get_json()
        # if "hola" in reques:
        #     print(reques['hola'], type(reques['hola']))
        # return productos, 200
        ps = ProductoModel.objects.all()
        return ProductoSchema(many=True).dump(ps), 200

    @classmethod
    def post(self):
        req = request.get_json()
        try:
            p = ProductoModel()
            if "nombre" in req:
                p.nombre = req["nombre"]
            if "precio_venta" in req:
                p.precio_venta = req["precio_venta"]
            if "precio_compra" in req:
                p.precio_compra = req["precio_compra"]
            if "categoria" in req:
                p.categoria = req["categoria"]
            if "imagen" in req:
                p.imagen = req["imagen"]
            p.save()
            # if "" in req:
            #     p. = req[""]
        except ValidationError as exc:
            print(exc.message)
            return {"message": "No se pudo crear el nuevo movimiento."}   
        return {'message': "Producto creado"}, 200


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

    @classmethod
    def post(self):
        req = request.get_json()
        try:
            p = PromocionModel()
            if "titulo" in req:
                p.titulo = req["titulo"]
            if "tipo" in req:
                p.tipo = req["tipo"]
            if "valor" in req:
                p.valor = req["valor"]
            if "productos_validos" in req:
                p.productos_validos = req["productos_validos"]
            if "puntos" in req:
                p.puntos = req["puntos"]
            if "sellos" in req:
                p.sellos = req["sellos"]
            if "imagen" in req:
                p.imagen = req["imagen"]
            p.save()
            # if "" in req:
            #     p. = req[""]
        except ValidationError as exc:
            print(exc.message)
            return {"message": "No se pudo crear el nuevo movimiento."}   
        return {'message': "Promocion creada"}, 200


class Promocion(Resource):
    @classmethod
    def get(self, id):
        print(promociones)
        for index, item in enumerate(promociones):
            print(item)
            if(item['_id'] ==  id):
                return item, 200
        return {'No existe una promocion con ese _id'}, 404


class TicketList(Resource):
    @classmethod
    def get(self):
        return tickets, 200

    @classmethod
    def post(self):
        req_json = request.get_json()
        req = VentaSchema().load(req_json)
        try:
            p = VentaModel()
            if "total" in req:
                p.total = req["total"]
            if "descuento" in req:
                p.descuento = req["descuento"]
            if "fecha" in req:
                p.fecha = req["fecha"]
            if "id_participante" in req:
                p.id_participante = req["id_participante"]
            if "promociones" in req:
                p.promociones = req["promociones"]
            if "detalle_venta" in req:
                p.detalle_venta = req["detalle_venta"]
            p.save()
            # if "" in req:
            #     p. = req[""]
        except ValidationError as exc:
            print(exc.message)
            return {"message": "No se pudo crear el nuevo movimiento."}   
        return {'message': "Venta (Ticket) creada"}, 200

class Ticket(Resource):
    @classmethod
    def get(self, id):
        for index, item in enumerate(tickets):
            print(item)
            if(item['_id'] ==  id):
                return item, 200
        return {'No existe un ticket con ese _id'}, 404