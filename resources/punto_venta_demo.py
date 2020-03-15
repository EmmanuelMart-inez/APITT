import json
import datetime as dt
import functools
import uuid
from bson.objectid import ObjectId
from flask import request
from flask_restful import Resource


# Establish a connection to the database.
connect("mongodb://localhost:27017/ej1")



# # class Bienvenida(Resource):
# #     pass

# fullPromo = 
# 	{
# 		nombre:  "Jueves 2x1",
# 		descripcion: "2x1 en bebidas calientes",
# 		descuento_porciento: 0.00,
# 		descuento_pesos: 0.00,
# 		descuento_producto: 0,
# 		descuento_categoria:  "BC1",
# 		fecha_creacion: ISODate("2019-01-01"),
# 		fecha_vigencia: ISODate("2019-01-01"),
# 		fecha_redencion: ISODate("2019-01-01"),
# 		imagen_miniatura: "/images/promo/n1.png",
# 		imagen_display: "/images/promo/display/n1.png",
# 		codigo_barras: "12121212121",
# 		codigo_qr: "aQ#ACszxc812vbb",
# 		id_participante: participante__id
# 	}



# # Promociones y premios por igual
# Promociones = {[
#     {
#         # 'imagen': "http..."
#         'tipo': '2x1', #3x1, Combo o paquete
#         "titulo": "Dos al precio de uno",
#         "id": "asd684a415s64d6asd",
#         "variacion": "mismo tipo"
#         "productos_validos": ["asd684a415s64d6asd","asd684a415s64d6asd","asd684a415s64d6asd","asd684a415s64d6asd"] #id_producto
#     },
#     {
#         'tipo': 'descuento',
#         "titulo": "30% en bebidas frapeé",
#         "id": "asd684a415s64d6asd",
#         "variante": "porcentage"
#         # "productos_validos": ["asd684a415s64d6asd","asd684a415s64d6asd","asd684a415s64d6asd","asd684a415s64d6asd"] #id_producto
#         'categoria': 'frapeé',
#     },
#     {
#         'tipo': 'descuento',
#         "titulo": "50% de descuento en la compra de un frappé Halloween",
#         "id": "asd684a415s64d6asd",
#         "variante": "producto"
#         # "productos_validos": ["asd684a415s64d6asd","asd684a415s64d6asd","asd684a415s64d6asd","asd684a415s64d6asd"] #id_producto
#         'categoria': 'frapeé',
#     },
#     {
#         'tipo': 'descuento',
#         "titulo": "50% de descuento en la compra superior a $200",
#         "id": "asd684a415s64d6asd",
#         "variante": "cantidad dinero"
#         # "productos_validos": ["asd684a415s64d6asd","asd684a415s64d6asd","asd684a415s64d6asd","asd684a415s64d6asd"] #id_producto
#         'categoria': 'frapeé',
#     },
#     {
#         'tipo': 'descuento',
#         "titulo": "50% de descuento en la compra 5 bebidas",
#         "id": "asd684a415s64d6asd",
#         "variante": "cantidad productos"
#         # "productos_validos": ["asd684a415s64d6asd","asd684a415s64d6asd","asd684a415s64d6asd","asd684a415s64d6asd"] #id_producto
#         'categoria': 'bebidas',
#     },
#     {
#         'tipo': 'descuento',
#         "titulo": "50% de descuento en la compra un BubbleCombo",
#         "id": "asd684a415s64d6asd",
#         "variante": "paquete productos"
#         # "productos_validos": ["asd684a415s64d6asd","asd684a415s64d6asd","asd684a415s64d6asd","asd684a415s64d6asd"] #id_producto
#         # 'categoria': 'combos',
#     },
#     {
#         'tipo': 'gratis',
#         "titulo": "Regalo de lealtad",
#         "id": "asd684a415s64d6asd",
#         "productos": ["asd684a415s64d6asd"] #id_producto
#     }
# ]}



# venta = {
# 		_id: venta__id,
# 		total: 150.50,
# 		fecha: ISODate("2020-06-06T10:00:00Z"),
# 		id_participante: participante__id,
# 		forma_pago: {
# 					nombre: "efectivo", 
# 					otros_detalles: "Datos de la terminal importantes"
# 					},
# 		qr: "asdaqwke923jl4jql0jqeqeq",
# 		descuento_general: 15.5,
# 		usuario_id_usuario: usuario__id,
# 		detalle_venta: [
# 						{
# 							cantidad: 2, 
# 							precio: 80.00,
# 							impuestos: 0.16,
# 							descuento_producto: 0.00,
# 							producto: [
# 										{
# 											codigo_barras: "02102102012",
# 											nombre : "Bubble Tea 600 ml",
# 											descripcion: "Bubbletea de temporada presentacion individual",
# 										}
# 									  ],
# 							importe: 74.16
# 					    },
# 					    {
# 							cantidad: 1, 
# 							precio: 80.00,
# 							impuestos: 0.16,
# 							descuento_producto: 0.00,
# 							producto: [
# 										{
# 											codigo_barras: "02102102012",
# 											nombre : "Bubble coffee 600 ml",
# 											descripcion: "Bubbletea de temporada presentacion individual"
# 										}
# 									  ],
# 							importe: 74.16
# 					    }
# 					   ]
# 	}

promociones = [
	{
		'_id': 1,
		'titulo': '50% de descuento en la compra de un frappé Halloween',
		'tipo': 'porcentaje',
		'valor': '0.5',
		'productos_validos': [2],
		'fecha_vigencia':  '2019-06-06T16:00:00Z'
	},
	{
		'_id': 2,
		'titulo': '50% de descuento sobre tu compra',
		'tipo': 'porcentaje compra',
		'valor': '0.5',
		'productos_validos': [],
		'fecha_vigencia':  '2019-06-06T16:00:00Z'
	},
	{
		'_id': 3,
		'titulo': '2x1 en bolipanes',
		'tipo': 'porcentaje',
		'valor': '0.5',
		'productos_validos': [1],
		'fecha_vigencia':  '2019-06-06T16:00:00Z'
	},
	{
		'_id': 3,
		'titulo': 'Llevate un bolipán gratis en la compra de 2 frappés Halloween,
		'tipo': 'combo',
		'valor': '1',  #id de promocion al 100%
		'productos_requeridos': [2, 2],
		# 'productos_validos': [2, 2],
		'fecha_vigencia':  '2019-06-06T16:00:00Z'
	}
] 

productos = [
	{
		'id': 1, 
		'nombre': 'bolipan', 
		'precio_venta': 50.50, 
		'categoria': 'Alimentos'
	},
	{
		'id': 2, 
		'nombre': 'frapeé halloween', 
		'precio_venta': 50.50, 
		'categoria': 'Alimentos'
	}
]


ticket = {
	id,
	total 
	fecha
	id_participante
	productos=[
		id,
		nombre,
		precio_venta
	]
	descuentos=[1,2,3,4]
}

	# porcentaje, combo, cantidad en pesos


class Promocion(Resource):
    pass


class Ticket(Resource):
    pass