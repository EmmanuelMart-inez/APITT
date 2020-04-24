from ma import ma
from marshmallow import Schema, fields, ValidationError

class PromocionSchema(ma.Schema):
    # nombre = fields.Str()
    _id = fields.Str()
    titulo = fields.Str()
    tipo = fields.Str()
    valor = fields.Float()
    productos_validos = fields.List(fields.Str(), default=[])
    puntos = fields.Float()
    sellos = fields.Integer()
    descripcion = fields.Str()
    descuento_porciento = fields.Float()
    descuento_pesos = fields.Float()
    descuento_producto = fields.Float()
    descuento_categoria = fields.Str()
    fecha_creacion = fields.DateTime()
    fecha_vigencia = fields.DateTime()
    fecha_redencion = fields.DateTime()
    imagen_miniatura = fields.URL()
    imagen_display = fields.URL()
    codigo_barras = fields.Str()
    codigo_qr = fields.Str()
    # id_participante = fields.ReferenceField(Participante)

    class Meta: 
        fields = (
            "_id",
            "titulo",
            "tipo",
            "valor",
            "productos_validos",
            "fecha_vigencia",
            "puntos",
            "sellos"
        )

class ProductoSchema(ma.Schema):
    _id = fields.Str()
    codigo_barras = fields.Str()
    nombre = fields.Str()
    stock = fields.Integer()
    precio_compra = fields.Float()
    tipo_de_ganancia = fields.Str()
    # Porcentaje fijo o por monto neto a mano
    precio_venta = fields.Float()
    porcentaje_ganancia = fields.Float()
    categoria = fields.Str()
    proveedor = fields.Str()
    atributos = fields.Str()
    
    class Meta: 
        fields = (
            "_id",
            "nombre",
            "precio_compra",
            "precio_venta",
            "categoria"
        )

class detalleVentaSchema(ma.Schema):
    cantidad = fields.Integer()
    precio = fields.Float()
    # impuestos = fields.Float()
    descuento_producto = fields.Integer()
    importe = fields.Integer()
    producto = fields.Nested(
        ProductoSchema)
    
    class Meta:
        fields = (
            "cantidad",
            "impuestos",
            "descuento_producto",
            "producto",
            "importe"
        )

class VentaSchema(ma.Schema):
    _id = fields.Str()
    total = fields.Float()
    promociones = fields.List(fields.Str())
    # subtotal = fields.Float
    # impuestos = fields.Float()
    # cambio = fields.Float()
    fecha = fields.DateTime()
    descuento = fields.Float()
    descuento_general = fields.Float()
    codigo_qr = fields.Str()
    # forma_pago = fields.EmbeddedDocumentField(
    #     FormaPagoModel)
    detalle_venta = fields.List( 
        fields.Nested(detalleVentaSchema), default=[])
    id_vendedor = fields.Str()
    id_participante = fields.Str()
    id_ticket_punto_venta = fields.Str()

    class Meta:
        fields = (
        "_id",
		"total",
        "descuento",
		"fecha",
		"id_participante",
        "promociones",
		"detalle_venta",
        "id_ticket_punto_venta"
        )