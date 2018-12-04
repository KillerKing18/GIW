# -*- coding: utf-8 -*-

##
## Carlos Bilbao, Mario Bocos, Álvaro López y David Élbez declaramos que esta solución es fruto exclusivamente
## de nuestro trabajo personal. No hemos sido ayudados por ninguna otra persona ni hemos
## obtenido la solución de fuentes externas, y tampoco hemos compartido nuestra solución
## con nadie. Declaramos además que no hemos realizado de manera deshonesta ninguna otra
## actividad que pueda mejorar nuestros resultados ni perjudicar los resultados de los demás.
##

import pymongo, hashlib, uuid, hashlib, pyotp, base64 ,pillow,qrcode

from pymongo import MongoClient
from bottle import post, get, route, run, template, request

mongoclient = MongoClient()
db = mongoclient.giw
collection = db['usuarios']

pimienta = "c6y]s4*u#L3r?tZ{3LYM95'vLq%DfmrF{'gjv[vs:B%!_FP3L)r$-r^;~swKcUabrcapata89"

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
# También genero una semilla en base 32 que usaré para un Time-Based One-Time Password Algorithm (TOTP). 
# TODO

def safe(password, sal):
   safepas = hashlib.sha512(password + sal).hexdigest()
   safepas = hashlib.pbkdf2_hmac('sha256', safepas, sal, 100000) # Algoritmo PBKDF2
   safepas = safepas + pimienta
   print("safepas => ", safepas)
   return safepas

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
   safepas = safe(query['password'], sal)

   usuario = {'name':query['name'],'nickname':query['nickname'],'country':query['country'],
	      'email':query['email'], 'password':safepas, 'sal':sal}
   collection.insert_one(usuario)

   return  "Bienvenido usuario " + query['name']


@post('/change_password')
def change_password():
    query = request.POST

    result = collection.find({'name':query['name']})

    # El usuario existe en la BBDD y coincide la contraseña
    if(result.count > 0 and safe(query['old_password'],result['sal']) == safe(result['password'], result['sal'])):
      sal = uuid.uuid4().hex # Actualizo sal
      collection.update_one({'name':query['name']},{'$set': {'password': safe(query['new_password'], sal), 'sal': sal}})
      return "La contraseña del usuario " + query['name'] + " ha sido modificada"
    else:
      return "Usuario o contraseña incorrectos"

@post('/login')
def login():
    query = request.POST
    result = collection.find({'name':query['name']})

    # El usuario existe en la BBDD y coincide la contraseña
    if(result.count > 0 and safe(query['password'],result['sal']) == safe(result['password'], result['sal'])):
      return "Bienvenido " query['name']
    else:
      return "Usuario o contraseña incorrectos"

##############
# APARTADO 2 # TODO http://blog.contraslash.com/doble-autenticacion-con-python/
##############

#
# Explicación detallada de cómo se genera la semilla aleatoria, cómo se construye
# la URL de registro en Google Authenticator y cómo se genera el código QR
# Necesito una semilla (o seed) en base 32, y para eso uso pyotp, luego preguntar por los números actuales con totp.now().
# Para generar el QR tengo que llamar a la URL de Google Authenticator con los parámetros del usuario y la semilla y generar 
# el propio QR gracias a pillow y qrcode 
# Mi QR podrá ya ser leido por Google Authenticator
#

@post('/signup_totp')
def signup_totp():
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
   safepas = safe(query['password'], sal)
   semilla = base64..b32encode(safepas.encode()).decode()
   #totp = pyotp.TOTP(SECRET_KEY_BASE_32) y totp.now() para un momento dado

   usuario = {'name':query['name'],'nickname':query['nickname'],'country':query['country'],
        'email':query['email'], 'password':safepas, 'sal':sal, 'semilla': semilla}
   collection.insert_one(usuario)

   qr "otpauth://totp/localhost::8080:signup_totp:" + query['name'] + "secret=" + semilla + "&issuer=" + query['name'] > qr.png

   return  "nombre = " + query['name'] + " semilla = " + semilla + " QR = " + qr.png


@post('/login_totp')
def login_totp():
  query = request.POST
  result = collection.find({'name':query['name']})
  totp = pyotp.TOTP(result['semilla'])

  # El usuario existe en la BBDD y coincide la contraseña
  if(result.count > 0 and safe(query['password'],result['sal']) == safe(result['password'], result['sal']) and totp.now() == query['semilla']):
       return "Bienvenido " query['name']
  else:
    return "Usuario o contraseña incorrectos"

if __name__ == "__main__":
    # NO MODIFICAR LOS PARÁMETROS DE run()
    run(host='localhost',port=8080,debug=True)
