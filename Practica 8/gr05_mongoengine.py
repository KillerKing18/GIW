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

	def clean(self):
		if(self.cantidad * self.precio_producto != self.precio_linea): # Esquema punto 3
			raise ValidationError("El precio no coincide con la muliplicacion de cantidades y precio")
		if(self.nombre != self.producto.nombre): # Esquema punto 4
			raise ValidationError("No coinciden los nombres de producto y linea de producto")
		return True

class Pedido(Document):
	precio_total = IntField(min_value=1,required=True)
	fecha = ComplexDateTimeField(required=True)
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
		if(len(self.ultimos_accesos) > 10): # No puede haber mas de 10
			raise ValidationError("No puede haber mas de 10 ultimos accesos")
		if(isnotValid(self.DNI)): # La funcion auxiliar comprueba que se cumple el formato del DNI nacional
			raise ValidationError("El DNI no tiene el formato correcto") # Esquema punto 1

def isnotValid(DNI):
	num = DNI[:8]
	num = int(num) % 23

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
	return False

def insertar():
	# Usuario 1
	producto1a = Producto(codigo_barras = "123456789", nombre = "Toalla", categoria_principal = 4, categorias_secundarias=[4, 5, 6])
	producto1a.save()
	producto2a = Producto(codigo_barras = "987654321", nombre = "Balon", categoria_principal = 3)
	producto2a.save()
	producto3a = Producto(codigo_barras = "ABCDEFGHI", nombre = "Sombrilla", categoria_principal = 1, categorias_secundarias=[1, 2, 3])
	producto3a.save()
	producto4a = Producto(codigo_barras = "472958205", nombre = "Helado", categoria_principal = 3, categorias_secundarias=[3, 4, 5])
	producto4a.save()
	producto5a = Producto(codigo_barras = "847295837", nombre = "Agua", categoria_principal = 7)
	producto5a.save()
	linea_pedido1a = Linea_Pedido(cantidad = 4, precio_producto = 2, nombre = "Toalla", precio_linea = 8, producto = producto1a)
	linea_pedido2a = Linea_Pedido(cantidad = 10, precio_producto = 5, nombre = "Balon", precio_linea = 50, producto = producto2a)
	linea_pedido3a = Linea_Pedido(cantidad = 7, precio_producto = 15, nombre = "Sombrilla", precio_linea = 105, producto = producto3a)
	linea_pedido4a = Linea_Pedido(cantidad = 10, precio_producto = 3, nombre = "Helado", precio_linea = 30, producto = producto4a)
	linea_pedido5a = Linea_Pedido(cantidad = 10, precio_producto = 1, nombre = "Agua", precio_linea = 10, producto = producto5a)
	pedido1a = Pedido(precio_total = 163, fecha = "2018,11,27,20,59,40,000000", lista_lineas = [linea_pedido1a, linea_pedido2a, linea_pedido3a])
	pedido1a.save()
	pedido2a = Pedido(precio_total = 40, fecha = "2015,3,20,01,45,33,000000", lista_lineas = [linea_pedido4a, linea_pedido5a])
	pedido2a.save()
	tarjeta1a = Tarjeta_Credito(nombre = "Juan Ramirez Perez", numero = "1572894830294827", mes_caducidad = "01", anio_caducidad = "22", codigo_verificacion = "012")
	tarjeta2a = Tarjeta_Credito(nombre = "Juan Ramirez Perez", numero = "4839285720195927", mes_caducidad = "02", anio_caducidad = "19", codigo_verificacion = "123")
	usuario1 = Usuario(DNI = "50346706M", nombre = "Juan", primer_apellido = "Ramirez", segundo_apellido = "Perez", fecha_nacimiento = ("1996, 04, 22"), ultimos_accesos = ["2018,11,27,19,59,40,000000", "2018,11,27,18,59,40,000000"], tarjetas_credito = [tarjeta1a, tarjeta2a], pedidos = [pedido1a, pedido2a])
	usuario1.save()
	
	# Usuario 2
	producto1b = Producto(codigo_barras = "843927583", nombre = "Tarjeta Grafica", categoria_principal = 2)
	producto1b.save()
	producto2b = Producto(codigo_barras = "843928573", nombre = "Placa base", categoria_principal = 15, categorias_secundarias=[15, 8, 6])
	producto2b.save()
	producto3b = Producto(codigo_barras = "573950392", nombre = "RAM", categoria_principal = 23, categorias_secundarias=[23, 46, 16])
	producto3b.save()
	producto4b = Producto(codigo_barras = "859396038", nombre = "Tornillo", categoria_principal = 12)
	producto4b.save()
	producto5b = Producto(codigo_barras = "950395732", nombre = "Alicate", categoria_principal = 47, categorias_secundarias=[47, 12])
	producto5b.save()
	producto6b = Producto(codigo_barras = "958305937", nombre = "Martillo", categoria_principal = 17)
	producto6b.save()
	producto7b = Producto(codigo_barras = "853954739", nombre = "Sierra", categoria_principal = 18, categorias_secundarias=[18, 20])
	producto7b.save()
	linea_pedido1b = Linea_Pedido(cantidad = 5, precio_producto = 200, nombre = "Tarjeta Grafica", precio_linea = 1000, producto = producto1b)
	linea_pedido2b = Linea_Pedido(cantidad = 5, precio_producto = 100, nombre = "Placa base", precio_linea = 500, producto = producto2b)
	linea_pedido3b = Linea_Pedido(cantidad = 5, precio_producto = 75, nombre = "RAM", precio_linea = 375, producto = producto3b)
	linea_pedido4b = Linea_Pedido(cantidad = 15, precio_producto = 1, nombre = "Tornillo", precio_linea = 15, producto = producto4b)
	linea_pedido5b = Linea_Pedido(cantidad = 2, precio_producto = 15, nombre = "Alicate", precio_linea = 30, producto = producto5b)
	linea_pedido6b = Linea_Pedido(cantidad = 2, precio_producto = 20, nombre = "Martillo", precio_linea = 40, producto = producto6b)
	linea_pedido7b = Linea_Pedido(cantidad = 1, precio_producto = 45, nombre = "Sierra", precio_linea = 45, producto = producto7b)
	pedido1b = Pedido(precio_total = 1875, fecha = "2017,03,07,19,35,22,000000", lista_lineas = [linea_pedido1b, linea_pedido2b, linea_pedido3b])
	pedido1b.save()
	pedido2b = Pedido(precio_total = 45, fecha = "2016,04,18,19,00,00,000000", lista_lineas = [linea_pedido4b, linea_pedido5b])
	pedido2b.save()
	pedido3b = Pedido(precio_total = 85, fecha = "2008,01,22,22,00,00,000000", lista_lineas = [linea_pedido6b, linea_pedido7b])
	pedido3b.save()
	tarjeta1b = Tarjeta_Credito(nombre = "Marcos Martinez", numero = "3859284029184938", mes_caducidad = "05", anio_caducidad = "24", codigo_verificacion = "999")
	tarjeta2b = Tarjeta_Credito(nombre = "Marcos Martinez", numero = "5948372059382942", mes_caducidad = "07", anio_caducidad = "30", codigo_verificacion = "888")
	tarjeta3b = Tarjeta_Credito(nombre = "Marcos Martinez", numero = "4837295830593850", mes_caducidad = "12", anio_caducidad = "20", codigo_verificacion = "777")
	usuario2 = Usuario(DNI = "58204938B", nombre = "Marcos", primer_apellido = "Martinez", fecha_nacimiento = ("1996, 04, 22"), tarjetas_credito = [tarjeta1b, tarjeta2b, tarjeta3b], pedidos = [pedido1b, pedido2b, pedido3b])
	usuario2.save()

	# Usuario 3
	usuario3 = Usuario(DNI = "84938293Y", nombre = "Pepe", primer_apellido = "Garcia", fecha_nacimiento = ("1965, 02, 15"))
	usuario3.save()

#TODO 
#	5
#	DNI (regex, extranjeros)
#	Tarjeta regex
#	Comprobar valor maximo y minimo para el mes de la tarjeta?
#	Hacer numeros de la tarjeta StringField o IntField?