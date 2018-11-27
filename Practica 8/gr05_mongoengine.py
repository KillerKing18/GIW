##
## Carlos Bilbao, Mario Bocos, Alvaro Lopez y David Elbez declaramos que esta solucion es fruto exclusivamente
## de nuestro trabajo personal. No hemos sido ayudados por ninguna otra persona ni hemos
## obtenido la solucion de fuentes externas, y tampoco hemos compartido nuestra solucion
## con nadie. Declaramos ademas que no hemos realizado de manera deshonesta ninguna otra
## actividad que pueda mejorar nuestros resultados ni perjudicar los resultados de los demas.
##
import mongoengine
from mongoengine import *
connect('giw_mongoengine')

class Producto(Document):
	codigo_barras = StringField(required=True, unique=True)
	nombre = StringField(required=True)
	categoria_principal = IntField(required=True, min_value = 0)
	categorias_secundarias = ListField(IntField(min_value = 0))

	def clean(self):
		# Debe tener el formato EAN_13
		if(isnotEANValid(self.codigo_barras)): # Esquema punto 5
			raise ValidationError("El codigo de barras no tiene el formato adecuado (EAN 13)")

		if(len(self.categorias_secundarias) > 0 and self.categorias_secundarias[0] != self.categoria_principal): # Esquema punto 6
			raise ValidationError("La categoria principal debe ser la primera en la lista de categorias secundarias")

class Linea_Pedido(EmbeddedDocument):
	cantidad = IntField(required=True)
	precio_producto = IntField(required=True)
	nombre = StringField(required=True)
	precio_linea = IntField(required=True)
	producto = ReferenceField(Producto, required=True)

	def es_valido(self):
		if(self.cantidad * self.precio_producto != self.precio_linea): # Esquema punto 3
			raise ValidationError("El precio no coincide con la muliplicacion de cantidades y precio")
		if(self.nombre != self.producto.nombre): # Esquema punto 4
			raise ValidationError("No coinciden los nombres de producto y linea de producto")
		return True

class Pedido(Document):
	precio_total = FloatField(min_value=1,required=True)
	fecha = ComplexDateTimeField(min_value=2018,required=True)
	lista_lineas = ListField(EmbeddedDocumentField(Linea_Pedido), required=True)

	def clean(self):
		if(self.precio_total != sumPrec(self.lista_lineas)): # La suma de los pedidos ser igual al total
			raise ValidationError("La suma de los productos no coincide con el precio total") # Esquema punto 2

class Tarjeta_Credito(EmbeddedDocument):
	nombre = StringField(required=True)
	numero = StringField(required=True, min_length = 16, max_length = 16, regex = "[0-9]")
	mes_caducidad = StringField(required=True, min_length = 2, max_length = 2, regex = "[0-9]")
	anio_caducidad = StringField(required=True, min_length = 2, max_length = 2, regex = "[0-9]")
	codigo_verificacion = StringField(required=True, min_length = 3, max_length = 3, regex = "[0-9]")

class Usuario(Document):
	DNI = StringField(required=True, unique=True, regex = "[0-9]+[A-Z]", min_length = 9, max_length = 9)
	nombre = StringField(required=True)
	primer_apellido = StringField(required=True)
	segundo_apellido = StringField()
	fecha_nacimiento = DateTimeField(required=True)
	ultimos_accesos = ListField(ComplexDateTimeField())
	tarjetas_credito = ListField(EmbeddedDocumentField(Tarjeta_Credito))
	pedidos = ListField(ReferenceField(Pedido, reverse_delete_rule = PULL)) # Articulo punto 7 -> reverse_delete_rule

	def clean(self):
		if(len(self.ultimos_accesos > 10)): # No puede haber mas de 10
			raise ValidationError("No puede haber mas de 10 ultimos accesos")
		if(isnotValid(self.DNI)): # La funcion auxiliar comprueba que se cumple el formato del DNI nacional
			raise ValidationError("El DNI no tiene el formato correcto") # Esquema punto 1

def isnotValid(DNI):
	num = DNI[:8]
	num = num % 23

	if num == 0:
		letra = "T"
	elif num == 1:
		letra = "R"
	elif num == 2:
		letra = "W"
	elif num == 3:
		letra = "A"
	elif num == 4:
		letra = "G"
	elif num == 5:
		letra = "M"
	elif num == 6:
		letra = "Y"
	elif num == 7:
		letra = "F"
	elif num == 8:
		letra = "P"
	elif num == 9:
		letra = "D"
	elif num == 10:
		letra = "X"
	elif num == 11:
		letra = "B"
	elif num == 12:
		letra = "N"
	elif num == 13:
		letra = "J"
	elif num == 14:
		letra = "Z"
	elif num == 15:
		letra = "S"
	elif num == 16:
		letra = "Q"
	elif num == 17:
		letra = "V"
	elif num == 18:
		letra = "H"
	elif num == 19:
		letra = "L"
	elif num == 20:
		letra = "C"
	elif num == 21:
		letra = "K"
	else:
		letra = "E"

	if letra != DNI[8:]: # No coincidente
		return True
	else:
		return False

def sumPrec(lista):
	sum = 0
	for i in lista:	# Sumamos los precios de cada elemento
		sum = sum + i.precio_linea
	return sum

def isnotEANValid(ean):
	# TODO - Codigo Python del Wiki?
	return False

	
###### INSERCIONES ######

producto1 = Producto(codigo_barras = "123456789", nombre = "Toalla", categoria_principal = 4, categorias_secundarias=[4, 5, 6])
producto1.save()
linea_pedido1 = Linea_Pedido(cantidad = 4, precio_producto = 2, nombre = "Toalla", precio_linea = 8, producto = producto1)
if linea_pedido1.es_valido():
	print("Valido")
else:
	print("Invalido")
# Hacer save sobre EmbeddedDocument no tiene efecto, asi que que pasa con clean



#TODO 
#	Formato EAN_13
