# -*- coding: utf-8 -*-
 
##
## Carlos Bilbao, Mario Bocos, Álvaro López y David Élbez declaramos que esta solución es fruto exclusivamente
## de nuestro trabajo personal. No hemos sido ayudados por ninguna otra persona ni hemos
## obtenido la solución de fuentes externas, y tampoco hemos compartido nuestra solución
## con nadie. Declaramos además que no hemos realizado de manera deshonesta ninguna otra
## actividad que pueda mejorar nuestros resultados ni perjudicar los resultados de los demás.
##
import pymongo
from pymongo import MongoClient
from bottle import get, route, run, template, request

# Conectamos nuestro servidor web al servidor de Mongo
mongoclient = MongoClient()

# Cogemos la colección de la BBDD
db = mongoclient.giw
usuarios = db['usuarios']
pedidos = db['pedidos']

#Pedidos:
#	_id = ObjectId(hex)
#	lineas = lista de elementos con precio(FloatField), nombre(StringField), total(FLoatFIeld) y cantidad (IntField)
#	cliente = IntField
#	total = FloatField
#Usuarios:
#	_id = IntFIeld
#	pais = StringField
#	edad = IntField
#	nombre = StringField
#	apellido1 = StringField
#	apellido2 = StringField

@get('/top_countries')
# http://localhost:8080/top_countries?n=3
def agg1():
	n = int(request.query.n)
	result = usuarios.aggregate([
		{"$group": {"_id": "$pais", "media": {"$avg":[]}}},
		{"$sort": {"count" : -1, "_id" : 1}},
		{"$limit": n}])

	return template("output", Cursor = result)


@get('/products')
# http://localhost:8080/products?min=2.34
def agg2():
	precio = float(request.query.min)
	result = pedidos.aggregate([
		{"$unwind": "$lineas"},
		{"$match": {"lineas.precio" : {"$gte" : precio}}},
		{"$group": {"_id": "$lineas.nombre", "count": {"$sum":"$lineas.cantidad"}, "precio": {"$first":"$lineas.precio"}}}
		])
	return template("output2", Cursor = result)

    
@get('/age_range')
# http://localhost:8080/age_range?min=80
def agg3():
	min_usuarios = int(request.query.min)
	result = usuarios.aggregate([
		{"$group": {"_id": "$pais", "count": {"$sum":1}, "edad_maxima": {"$max":"$edad"}, "edad_minima": {"$min":"$edad"}}},
		{"$match": {"count" : {"$gte" : min_usuarios}}},
		{"$addFields": {"rango": {"$subtract": ["$edad_maxima", "$edad_minima"]}}},
		{"$sort": {"rango" : -1, "_id" : 1}}])
	
	return template("output3", Cursor = result)
    

@get('/avg_lines')
# http://localhost:8080/avg_lines
def agg4():
	result = usuarios.aggregate([
		{"$lookup": {"from": "pedidos", "localField":"_id", "foreignField":"cliente", "as":"pedidos"}},
		{"$group": {"_id": "$pais"}}])
	#pedidos.lineas.cantidad
	return template("output4", Cursor = result)
    
    
@get('/total_country')
# http://localhost:8080/total_country?c=Alemania
def agg5():
    pass
    
        
if __name__ == "__main__":
    # No cambiar host ni port ni debug
    run(host='localhost',port=8080,debug=True)
