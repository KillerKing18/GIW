from mongoengine import connect
connect('giw_mongoengine')

class Usuario(Document):
	DNI = StringField(required=True, unique=True)
	nombre = StringField(required=True)
	primer_apellido = StringField(required=True)
	segundo_apellido = StringField()
	fecha_nacimiento = DateTimeField(required=True)
	ultimos_accesos = ListField(ComplexDateTimeField())
	tarjetas_credito = ListField(EmbeddedDocumentField(Tarjeta_Credito))
	pedidos = ListField(ReferenceField(Pedido, reverse_delete_rule = PULL))
	
class Tarjeta_Credito(EmbeddedDocument):
	nombre = StringField(required=True)
	numero = StringField(required=True, min_length = 16, max_length = 16, regex = "[0-9]") # Con StringField podemos asignar cuántos dígitos queremos exactamente (length)
	mes_caducidad = StringField(required=True, min_length = 2, max_length = 2, regex = "[0-9]")
	anio_caducidad = StringField(required=True, min_length = 2, max_length = 2, regex = "[0-9]")
	codigo_verificacion = StringField(required=True, min_length = 3, max_length = 3, regex = "[0-9]")
	
