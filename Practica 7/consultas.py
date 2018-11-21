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
	querys = request.query_string.split('&')

	for item in querys:
		item = item.split('=')
		listaComparar.append(item[0])

	for item in listaComparar:
		if(item != 'name' and item != 'surname' and item != 'birthdate'):
			if(item == ''):
				return '''<p> Campos vacios! </p>'''
			else:
				return '''<p>Has introducido mal el campo {{item}}</p>'''

	#Obtenemos los campos de la URL y dependiendo de cuales se hayan introducido realizamos la consulta
	#Lo de capitalize es porque la URL te pone el nombre en minusculas y si no lo pones con mayuscula Mongo no te lo encuentra(Ej:luz != Luz)
	nombre = request.query.name.capitalize()
	apellido = request.query.surname.capitalize()
	fecha = request.query.birthdate

	if(nombre != "" and apellido != "" and fecha != ""):
		result = collection.find({'name':nombre, 'surname':apellido,'birthdate':fecha})
	elif(nombre != "" and apellido != "" and fecha == ""):
		result = collection.find({'name':nombre, 'surname':apellido})
	elif(nombre != "" and apellido == "" and fecha != ""):
		result = collection.find({'name':nombre,'birthdate':fecha})
	elif(nombre == "" and apellido != "" and fecha != ""):
		result = collection.find({'surname':apellido,'birthdate':fecha})
	elif(nombre == "" and apellido != "" and fecha == ""):
		result = collection.find({'surname':apellido})
	elif(nombre == "" and apellido == "" and fecha != ""):
		result = collection.find({'birthdate':fecha})
	elif(nombre != "" and apellido == "" and fecha == ""):
		result = collection.find({'name':nombre})
	else:
		return '''<p>Error! Vacio</p>'''

	#Datos de la consulta
	#Para cada elemento del result estos serian los campos de su tabla
	if result.count() > 0:
		output = template("output", Cursor = result, Elementos = result.count())
		return output
	else:
		return '''<p>No se han encontrado resultados</p>'''

@get('/find_email_birthdate')
def email_birthdate():
	#Muestra id, email y birthdate de usuarios nacidos entre fecha from y to (ambas) Mostrar tabla con 3 columnas, num encontrados
	#Cogemos los datos
	fechaInicio = request.query['from']
	fechaFin = request.query.to

	#Consulta de mongo
	result = collection.find({'birthdate': {"$gte":fechaInicio, "$lte":fechaFin}})

    # http://localhost:8080/find_email_birthdate?from=1973-01-01&to=1990-12-31
	if result.count() > 0:
		output = template("output2", Cursor = result, Elementos = result.count())
		return output
	else:
		return '''<p>No se han encontrado resultados</p>'''

@get('/find_country_likes_limit_sorted')
def find_country_likes_limit_sorted():
    
	#http://localhost:8080/find_country_likes_limit_sorted?country=Irlanda&likes=movies,animals&limit=4&ord=asc

	listaComparar = []
	querys = request.query_string.split('&') #Obtenemos todos los campos de la URL

	for item in querys:
		item = item.split('=')
		listaComparar.append(item[0])

	for item in listaComparar:
		print(item)
		if(item != 'country' and item != 'likes' and item != 'limit' and item != 'ord'):
			if(item == ''):
				return '''<p> Campos vacios! </p>'''
			else:
				return '''<p>Has introducido mal el campo {{item}}</p>'''

	pais = request.query.country.capitalize()
	likes = request.query.likes
	limit = request.query.limit
	orden = request.query.ord

	likes = likes.split(",")

	if(pais != "" and likes != "" and limit != "" and orden == "asc"):
		result = collection.find({'address.country': pais, 'likes': {"$all" :likes}}).sort([("birthdate", 1)]).limit(int(limit))
	elif(pais != "" and likes != "" and limit != "" and orden == "desc"):
		result = collection.find({'address.country': pais, 'likes': {"$all" :likes}}).sort([("birthdate", -1)]).limit(int(limit))
	else:
		return '''<p>Has introducido mal un campo</p>'''

	if result.count() > 0:
		output = template("output", Cursor = result, Elementos = result.count())
		return output
	else:
		 return '''<p>No se han encontrado resultados</p>'''


@get('/find_birth_month')
def find_birth_month():
	# http://localhost:8080/find_birth_month?month=abril
	
	#Vemos si el campo de la URL es month
	listaComparar = []
	querys = request.query_string.split('&')

	for item in querys:
		item = item.split('=')
		listaComparar.append(item[0])

	for item in listaComparar:
		if(item != 'month'):
			if(item == ''):
				 return '''<p> Campos vacios! </p>'''
			else:
			       	return '''<p>Has introducido mal el campo {{item}}</p>'''

	nacimiento = request.query.month

	if(nacimiento == "enero"):
		nacimiento = 1
	elif(nacimiento == "febrero"):
		nacimiento = 2
	elif(nacimiento == "marzo"):
		nacimiento = 3
	elif(nacimiento == "abril"):
		nacimiento = 4
	elif(nacimiento == "mayo"):
		nacimiento = 5
	elif(nacimiento == "junio"):
		nacimiento = 6
	elif(nacimiento == "julio"):
		nacimiento = 7
	elif(nacimiento == "agosto"):
		nacimiento = 8
	elif(nacimiento == "septiembre"):
		nacimiento = 9
	elif(nacimiento == "octubre"):
		nacimiento = 10
	elif(nacimiento == "noviembre"):
		nacimiento = 11
	elif(nacimiento == "diciembre"):
		nacimiento = 12
	else:
		return '''<p>NO es un mes correcto!</p>'''

	nacimiento = "/" + str(nacimiento) + "/"

	if(nacimiento != ""): 
		result = collection.find({'birthdate': nacimiento}).sort([("birthdate", 1)])
	else:
		return '''<p>Error! Vacio</p>'''

	if result.count() > 0:
		output = template("output", Cursor = result, Elementos = result.count())
		return output
	else:
		 return '''<p>No se han encontrado resultados</p>'''


@get('/find_likes_not_ending')
def find_likes_not_ending():
	
	# http://localhost:8080/find_likes_not_ending?ending=s
	
	import re

	sufijo = request.query['ending'] #Obtenemos el campo de la URL
	sufijo = sufijo + "$"

	result = collection.find({'likes': {"$not": re.compile(sufijo)}})
	
	if result.count() > 0:
		output = template("output", Cursor = result, Elementos = result.count())
		return output
	else:
		return '''<p>No se han encontrado resultados</p>'''


@get('/find_leap_year')
def find_leap_year():
	# http://localhost:8080/find_leap_year?exp=20
	
	#Cogemos los datos
	expire = request.query.exp
	listaAux = []
	#Consulta de mongo
	result = collection.find({'credit_card.expire.year': expire})	#,{esBisiesto('birthdate'[:4]): True })
	
	for elem in result:
		fecha = elem['birthdate'][:4] #Cogemos solo el año
		if esBisiesto(fecha): 
			listaAux.append(elem)
	#Datos de la consulta
	#Para cada elemento del result estos serian los campos de su tabla
	if len(listaAux) > 0:
		output = template("output", Cursor = listaAux, Elementos = len(listaAux))
		return output
	else:
		return '''<p>No se han encontrado resultados</p>'''

def esBisiesto(year):
	return (int(year) % 100 != 0 and int(year) % 4 == 0) or (int(year) % 400 == 0)

###################################
# NO MODIFICAR LA LLAMADA INICIAL #
###################################
if __name__ == "__main__":
	run(host = 'localhost', port = 8080, debug = True)