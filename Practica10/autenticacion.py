# -*- coding: utf-8 -*-

##
## Carlos Bilbao, Mario Bocos, Álvaro López y David Élbez declaramos que esta solución es fruto exclusivamente
## de nuestro trabajo personal. No hemos sido ayudados por ninguna otra persona ni hemos
## obtenido la solución de fuentes externas, y tampoco hemos compartido nuestra solución
## con nadie. Declaramos además que no hemos realizado de manera deshonesta ninguna otra
## actividad que pueda mejorar nuestros resultados ni perjudicar los resultados de los demás.
##

import pymongo, hashlib, uuid, hashlib, pyotp, base64,qrcode, pyqrcode
from pymongo import MongoClient
from bottle import post, get, route, run, template, request
from passlib.totp import TOTP, generate_secret
from passlib.exc import TokenError, MalformedTokenError

mongoclient = MongoClient()
db = mongoclient.giw
collection = db['usuarios']

pimienta = "c6y]s4*u#L3r?tZ{3LYM95'vLq%DfmrF{'gjv[vs:B%!_FP3L)r$-r^;~swKcUabrcapata89"

secret = generate_secret()
TotpFactory = TOTP.using(secrets={"1":secret})

totpCounter = 0

##############
# APARTADO 1 #
##############

# MECANISMO DE PROTECCIÓN DE CONTRASEÑAS:
#
# Almacenar las contraseñas en la BBDD de Mongo sin cifrado expone a los usuarios.
# Para almacenar la contraseña de manera segura en la BBDD guardo ésta de la siguiente manera:
# El hash de la contraseña (con SHA512) + sal (generación de cadena aleatoria) + pimienta (cadena de texto estática)
# Además, quiero evitar Brute Force, y para ello uso un algoritmo de ralentizado (PBKDF2)
# La función de hashlib se encarga de añadir la sal
#.

def safe(password, sal):
    safepas = hashlib.sha512((password + sal + pimienta).encode("utf-8")).hexdigest()
    safepas = bytes(safepas,'utf-8')
    sal     = bytes(sal, 'utf-8')
    hashlib.pbkdf2_hmac('sha256', safepas, sal, 100000) # Algoritmo PBKDF2
    #print("safepas => ", safepas)
    return safepas

@post('/signup')
def signup():
    query = request.POST
    # tenemos: name, nickname, country, email, password, password2

    if(query['password'] != query['password2']):
           return '''<p>Las contraseñas no coinciden</p>'''

    if(query['nickname'] != ""):
        result = collection.find({'nickname':query['nickname']})
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

    result = collection.find({'nickname':query['nickname']}) 

    # El usuario existe en la BBDD y coincide la contraseña

    for val in result: # Only one name
        prevSal = val['sal']
        prevPas = val['password']

    if(result.count() > 0 and prevPas == safe(query['old_password'], prevSal)):
        sal = uuid.uuid4().hex # Actualizo sal
        collection.update_one({'nickname':query['nickname']},{'$set': {'password': safe(query['new_password'], sal), 'sal': sal}})
        return "La contraseña del usuario " + query['nickname'] + " ha sido modificada"
    else:
        return "Usuario o contraseña incorrectos"

@post('/login')
def login():
    query = request.POST
    result = collection.find({'nickname':query['nickname']})

    for val in result: # Only one name
        prevSal = val['sal']
        prevPas = val['password']

    # El usuario existe en la BBDD y coincide la contraseña
    if(result.count() > 0 and prevPas == safe(query['password'], prevSal)):
        return "Bienvenido " + query['nickname']
    else:
        return "Usuario o contraseña incorrectos"

##############
# APARTADO 2 # IDEAS -> http://blog.contraslash.com/doble-autenticacion-con-python/
##############

# 
#  Genero una semilla en base 32 que usaré para un Time-Based One-Time Password Algorithm (TOTP).
#  Se la proporciono al usuario para que al hacer login pueda darme el valor temporal,
#  si este es correcto (además de la contraseña) le daré acceso al usuario.
#  Info útil -> https://passlib.readthedocs.io/en/stable/narr/totp-tutorial.html
#

@post('/signup_totp')
def signup_totp():
    query = request.POST
    # tenemos: name, nickname, country, email, password, password2


    if(query['password'] != query['password2']):
           return '''<p>Las contraseñas no coinciden</p>'''

    if(query['nickname'] != ""):
        result = collection.find({'nickname':query['nickname']})
        if(result.count() > 0):
              return '''<p>El alias de usuario ya existe</p>'''
    else:
        return '''<p>No puedes usar un nombre vacio</p>'''

    sal = uuid.uuid4().hex
    safepas = safe(query['password'], sal)
    semilla = base64.b32encode(safepas).decode()

    totp = TotpFactory.new()
    uri = totp.to_uri(issuer="localhost",label="username")
    qr = pyqrcode.create(uri)
    print(qr.terminal())
    qr = qr.text()

    usuario = {'name':query['name'],'nickname':query['nickname'],'country':query['country'],
        'email':query['email'], 'password':safepas, 'sal':sal, 'semilla': semilla, 'key': qr}
    collection.insert_one(usuario)

    return  "<p>nombre = " + query['name'] + "<p> semilla = " + semilla + "</p><b> REVISA LA TERMINAL PARA VER EL QR </b>" 

@post('/login_totp')
def login_totp():
    query = request.POST
    result = collection.find({'nickname':query['nickname']})

    for val in result: # Only one name
        prevSal = val['sal']
        prevPas = val['password']
        source  =  val['key']

    token = query['totp']
    last_counter = totpCounter

    try:
        #match = TotpFactory.verify(token, source, last_counter=last_counter)
        pass #TODO
    except MalformedTokenError as err:
        return '<p>malformed token!</p>'
    except TokenError as err:
        return '<p>Invalid or reused token </p>'
    else:
        # El usuario existe en la BBDD y coincide la contraseña
        if(result.count() > 0 and prevPas == safe(query['password'], prevSal)):
            return "Bienvenido " + query['nickname']
        else:
            return "Usuario o contraseña incorrectos"

if __name__ == "__main__":
    # NO MODIFICAR LOS PARÁMETROS DE run()
    run(host='localhost', port=8080, debug = True)
