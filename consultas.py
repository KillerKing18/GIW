# -*- coding: utf-8 -*-

##
## Carlos Bilbao, Mario Bocos, Álvaro López y David Élbez declaramos que esta soluci´on es fruto exclusivamente
## de nuestro trabajo personal. No hemos sido ayudados por ninguna otra persona ni hemos
## obtenido la soluci´on de fuentes externas, y tampoco hemos compartido nuestra soluci´on
## con nadie. Declaramos adem´as que no hemos realizado de manera deshonesta ninguna otra
## actividad que pueda mejorar nuestros resultados ni perjudicar los resultados de los dem´as.
##
import pymongo
from pymongo import MongoClient
from bottle import get, route, run, template, request

# Conectamos nuestro servidor web al servidor de Mongo
mongoclient = MongoClient()

# Cogemos la colección de la BBDD
db = mongoclient.giw
collection = db['usuarios']

@get('/find_users')
def find_users():
    # Todas las combinaciones de name, surname y/o birthdate
    # http://localhost:8080/find_users?name=Luz
	# http://localhost:8080/find_users?name=Luz&surname=Romero
    # http://localhost:8080/find_users?name=Luz&surname=Romero&birthdate=2006-08-14
	
	#Vemos si los campos de la URL son name, surname o birthdate
	listaComparar = []
	querys = request.query_string #Obtenemos todos los campos de la URL
	querys2 = querys.split('&')
	for item in querys2:
		item = item.split('=')
		listaComparar.append(item[0])
	valido = True
	for item in listaComparar:
		if(item != 'name' and item != 'surname' and item != 'birthdate'):	#Ver si se han introducido otros campos que no son name surname o birthdate
			valido = False
			return '''<p>Has introducido un campo no válido</p>'''
	if(valido):
		#Obtenemos los campos de la URL y dependiendo de cuales se hayan introducido realizamos la consulta
		#Lo de capitalize es porque la URL te pone el nombre en minusculas y si no lo pones con mayuscula Mongo no te lo encuentra(Ej:luz != Luz)
		nombre = request.query.name
		apellido = request.query.surname
		fecha = request.query.birthdate
		print("Busqueda por nombre", nombre.capitalize(), ", apellido", apellido.capitalize(), ", y fecha", fecha)
		
		if(nombre != "" and apellido != "" and fecha != ""):
			result = collection.find({'name':nombre.capitalize(), 'surname':apellido.capitalize(),'birthdate':fecha})
		elif(nombre != "" and apellido != "" and fecha == ""):
			result = collection.find({'name':nombre.capitalize(), 'surname':apellido.capitalize()})
		elif(nombre != "" and apellido == "" and fecha != ""):
			result = collection.find({'name':nombre.capitalize(),'birthdate':fecha})
		elif(nombre == "" and apellido != "" and fecha != ""):
			result = collection.find({'surname':apellido.capitalize(),'birthdate':fecha})
		elif(nombre == "" and apellido != "" and fecha == ""):
			result = collection.find({'surname':apellido.capitalize()})
		elif(nombre == "" and apellido == "" and fecha != ""):
			result = collection.find({'birthdate':fecha})
		elif(nombre != "" and apellido == "" and fecha == ""):
			result = collection.find({'name':nombre.capitalize()})
		else:
			return '''<p>Los tres campos estan vacios</p>'''
		
		#Numero de usuarios devueltos por la consulta
		numElems = 0 
		for elem in result:
			numElems = numElems + 1
		#Datos de la consulta
		#Para cada elemento del result estos serian los campos de su tabla
		for elem in result:
			nombreUsuario = elem['_id']
			email = elem['email']
			paginaWeb = elem['webpage']
			tarjetaCredito = elem['credit_card'] + " " + elem['expire'] + " " + elem['number']
			hash = elem['password']
			nombre = elem['name']
			apellido = elem['surname']
			direccion = elem['address'] + " " + elem['country'] + " " + elem['zip'] + " " + elem['street'] + elem['num'] 
			aficiones = elem['likes']
			fechaNacimiento = elem['birthdate']
		#Tabla con los datos(faltaria hacer una tabla de todas las subtablas, que no se como se hace)
		return '''<table>
			<tr>
				<th>Nombre de usuario</th> %nombreUsuario
				<th>E-mail</th>
				<th>Página web</th>
				<th>Tarjeta de crédito</th>
				<th>Hash de contraseña</th>
				<th>Nombre</th>
				<th>Apellido</th>
				<th>Dirección</th>
				<th>Aficiones</th>
				<th>Fecha de nacimiento</th>
			</tr>
		</table>'''
		
@get('/find_email_birthdate')
def email_birthdate():
	print("hola")
    # http://localhost:8080/find_email_birthdate?from=1973-01-01&to=1990-12-31


@get('/find_country_likes_limit_sorted')
def find_country_likes_limit_sorted():
     print("hola")
	# http://localhost:8080/find_country_likes_limit_sorted?country=Irlanda&likes=movies,animals&limit=4&ord=asc


@get('/find_birth_month')
def find_birth_month():
	 print("hola")
  # http://localhost:8080/find_birth_month?month=abril


@get('/find_likes_not_ending')
def find_likes_not_ending():
	 print("hola")
  # http://localhost:8080/find_likes_not_ending?ending=s


@get('/find_leap_year')
def find_leap_year():
	 print("hola")
  # http://localhost:8080/find_leap_year?exp=20


###################################
# NO MODIFICAR LA LLAMADA INICIAL #
###################################
if __name__ == "__main__":
    run(host = 'localhost', port = 8080, debug = True)
