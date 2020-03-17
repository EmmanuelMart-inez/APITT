from pymodm import MongoModel, EmbeddedMongoModel, ReferenceField, fields, connect

connect('mongodb://localhost:27017/ej1')


class SubCategoriaModel(EmbeddedMongoModel):
    codigo = fields.CharField()
    nombre = fields.CharField()
    descripcion = fields.CharField()
    imagen = fields.URLField()


class CategoriaModel(EmbeddedMongoModel):
    codigo = fields.CharField()
    nombre = fields.CharField()
    descripcion = fields.CharField()
    subcategoria = fields.EmbeddedDocumentListField(
        SubCategoriaModel, default=[])
    imagen = fields.URLField()


class ProveedorModel(MongoModel):
    nombre_compania = fields.CharField()
    nombre_contacto = fields.CharField()
    direccion = fields.CharField()
    ciudad = fields.CharField()
    region = fields.CharField()
    codigo_postal = fields.IntegerField()
    pais = fields.CharField()
    telefono = fields.BigIntegerField()
    imagen = fields.URLField()


"""Descripción de los tipos de atributos 
    que puede tener un producto
i,e. 
[Atributos]
    atributos: [
					{
[AtributoDictList] ->   ingredientes: {
										ingrediente: "Azucar",
										ingrediente: "agua", 
										ingrediente: "té"
									},
[AtributoDict] -> 		presentacion: "Envase 500ml",
					},
					{
[AtributoMagnitudDict] -> nombre: "Valor en Bubblies",
						valor: "50",
						unidades: "bubblies"
					}
				]
"""


class AtributoDict(EmbeddedMongoModel):
    nombre = fields.CharField()
    descripcion = fields.CharField()


class AtributoDictList(EmbeddedMongoModel):
    nombre = fields.CharField()
    list_atributos_dict = fields.EmbeddedDocumentListField(
        AtributoDict, default=[])


class AtributoMagnitudDict(EmbeddedMongoModel):
    nombre = fields.CharField()
    valor = fields.FloatField()
    unidades = fields.FloatField()
    descripcion = fields.CharField()
    #estado = fields.Boolean()


class Atributos(EmbeddedMongoModel):
    dict = fields.EmbeddedDocumentListField(
        AtributoDict, default=[])
    dics = fields.EmbeddedDocumentListField(
        AtributoDictList, default=[])
    magn = fields.EmbeddedDocumentListField(
        AtributoMagnitudDict, default=[])


class ProductoModel(MongoModel):
    codigo_barras = fields.CharField()
    nombre = fields.CharField()
    stock = fields.IntegerField()
    precio_compra = fields.FloatField()
    tipo_de_ganancia = fields.CharField()
    # Porcentaje fijo o por monto neto a mano
    precio_venta = fields.FloatField()
    porcentaje_ganancia = fields.FloatField()
    categoria = fields.CharField()
    proveedor = fields.CharField()
    atributos = fields.CharField()
    # categoria = fields.EmbeddedDocumentListField(
    #     CategoriaModel, default=[])
    # proveedor = fields.ReferenceField(ProveedorModel)
    # atributos = fields.EmbeddedDocumentListField(
    #     Atributos, default=[])


class CatalogoModel(MongoModel):
    tipo = fields.CharField()
    imagen = fields.URLField()
    titulo = fields.CharField()
    descripcion = fields.CharField()
    fecha_vigencia = fields.DateTimeField()
    #id_producto = fields.ReferenceField(Producto)

    #TODO: Agregar metodos DAO