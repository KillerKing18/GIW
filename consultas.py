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
from bottle import get, route, run, template

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
	name = "NULL"
	surname = "NULL"
	birthdate = "NULL"
	name = request.headers.get('name')
	print(name)
	#result = collection.find({name: 'Pepe', surname: '', birthdate: '1971-02-03'})
	#print(result)

@get('/find_email_birthdate')
def email_birthdate():
    # http://localhost:8080/find_email_birthdate?from=1973-01-01&to=1990-12-31


@get('/find_country_likes_limit_sorted')
def find_country_likes_limit_sorted():
    # http://localhost:8080/find_country_likes_limit_sorted?country=Irlanda&likes=movies,animals&limit=4&ord=asc


@get('/find_birth_month')
def find_birth_month():
  # http://localhost:8080/find_birth_month?month=abril


@get('/find_likes_not_ending')
def find_likes_not_ending():
  # http://localhost:8080/find_likes_not_ending?ending=s


@get('/find_leap_year')     
def find_leap_year():
  # http://localhost:8080/find_leap_year?exp=20


###################################
# NO MODIFICAR LA LLAMADA INICIAL #
###################################
if __name__ == "__main__":
    run(host = 'localhost', port = 8080, debug = True)
