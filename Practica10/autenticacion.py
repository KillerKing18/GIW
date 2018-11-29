# -*- coding: utf-8 -*-

##
## Carlos Bilbao, Mario Bocos, Álvaro López y David Élbez declaramos que esta solución es fruto exclusivamente
## de nuestro trabajo personal. No hemos sido ayudados por ninguna otra persona ni hemos
## obtenido la solución de fuentes externas, y tampoco hemos compartido nuestra solución
## con nadie. Declaramos además que no hemos realizado de manera deshonesta ninguna otra
## actividad que pueda mejorar nuestros resultados ni perjudicar los resultados de los demás.
##

import pymongo, hashlib, uuid, hashlib
from pymongo import MongoClient
from bottle import post, get, route, run, template, request

mongoclient = MongoClient()
db = mongoclient.giw
collection = db['usuarios']

pimienta = "c6y]s4*u#L3r?tZ{3LYM95'vLq%DfmrF{'gjv[vs:B%!_FP3L)r$-r^;~s\&cUabrcapata89"

##############
# APARTADO 1 #
##############

# MECANISMO DE PROTECCIÓN DE CONTRASEÑAS:
#
# Almacenar las contraseñas en la BBDD de Mongo sin cifrado expone a los usuarios.
# Para almacenar la contraseña de manera segura en la BBDD guardo ésta de la siguiente manera:
# El hash de la contraseña (con SHA512) + sal (generación de cadena aleatoria) + pimienta (cadena de texto estática)
# Además, para evitar Brute Force uso un algoritmo de ralentizado (PBKDF2)
# La función de hashlib se encarga de añadir la sal
# TODO

@post('/signup')
def signup():
   query = request.POST
   # tenemos: name, nickname, country, email, password, password2

   if(query['password'] != query['password2']):
	return '''<p>Las contraseñas no coinciden</p>'''

   if(query['name'] != ""):
   	result = collection.find({'name':query['name']})
	if(result.count() > 0):
		return '''<p>El alias de usuario ya existe</p>'''
   else:
		return '''<p>No puedes usar un nombre vacio</p>'''

   sal = uuid.uuid4().hex
   safepas = hashlib.sha512(query['password'] + sal).hexdigest()
   safepas = hashlib.pbkdf2_hmac('sha256', safepas, sal, 100000) # Algoritmo PBKDF2
   safepas = safepas + pimienta
   print("safepas => ", safepas)
   usuario = {'name':query['name'],'nickname':query['nickname'],'country':query['country'],
	      'email':query['email'], 'password':safepas, 'sal':sal}
   collection.insert_one(usuario)

   return  "Bienvenido usuario " + query['name']


@post('/change_password')
def change_password():
    # Update sal
    pass


@post('/login')
def login():
    pass

##############
# APARTADO 2 # TODO
##############

#
# Explicación detallada de cómo se genera la semilla aleatoria, cómo se construye
# la URL de registro en Google Authenticator y cómo se genera el código QR
#

@post('/signup_totp')
def signup_totp():
    pass


@post('/login_totp')
def login_totp():
    pass

if __name__ == "__main__":
    # NO MODIFICAR LOS PARÁMETROS DE run()
    run(host='localhost',port=8080,debug=True)
