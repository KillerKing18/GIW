from mongoengine import connect
connect('giw_mongoengine')

class Usuario(Document):
	DNI = StringField(required=True, unique=True)
	nombre = StringField(required=True)
	primer_apellido = StringField(required=True)
	segundo_apellido = StringField()
	fecha_nacimiento = DateTimeField(required=True)
	ultimos_accesos = ListField(ComplexDateTimeField()) # Hacer de longitud 10
	tarjetas_credito = ListField(EmbeddedDocumentField(Tarjeta_Credito))
	pedidos = ListField(ReferenceField(Pedido, reverse_delete_rule = PULL))
	
class Tarjeta_Credito(EmbeddedDocument):
	nombre = StringField(required=True)
	numero = StringField(required=True, min_length = 16, max_length = 16, regex = "[0-9]") # Con StringField podemos asignar cuántos dígitos queremos exactamente (length)
	mes_caducidad = StringField(required=True, min_length = 2, max_length = 2, regex = "[0-9]")
	anio_caducidad = StringField(required=True, min_length = 2, max_length = 2, regex = "[0-9]")
	codigo_verificacion = StringField(required=True, min_length = 3, max_length = 3, regex = "[0-9]")
	
class Pedido(Document):
	precio_total = IntField(required=True)
	fecha = ComplexDateTimeField(required=True)
	lista_lineas = ListField(EmbeddedDocumentField(Linea_Pedido, required=True))
	
class Linea_Pedido(EmbeddedDocument):
	cantidad = IntField(required=True)
	precio_producto = IntField(required=True)
	nombre = StringField(required=True)
	precio_linea = IntField(required=True)
	producto = ReferenceField(Producto, required=True)

class Producto(Document):
	codigo_barras = StringField(required=True, unique=True) # Formato EAN-13
	nombre = StringField(required=True)
	categoria_principal = IntField(required=True) # Numero natural
	categorias_secundarias = ListField(IntField) # Numeros naturales