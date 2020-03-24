
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
