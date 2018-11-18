@get('/find_country_likes_limit_sorted')
def find_country_likes_limit_sorted():
    
	#http://localhost:8080/find_country_likes_limit_sorted?country=Irlanda&likes=movies,animals&limit=4&ord=asc

    listaComparar = []
	querys = request.query_string.split('&') #Obtenemos todos los campos de la URL

	for item in querys:
		item = item.split('=')
		listaComparar.append(item[0])

	for item in listaComparar:
		if(item != 'country' or item != 'likes' or item != 'limit' or item != 'ord'):
			if(item == ''):
				 return '''<p> Campos vacios! </p>'''
			else:
			       	return '''<p>Has introducido mal el campo {{item}}</p>'''

	pais = request.query.country.capitalize()
	likes = request.query.likes
	limit = request.query.limit
	orden = request.query.ord 

	if(pais != "" and likes != "" and limit != "" and orden == "asc"):
		result = collection.find({'address.country': pais, likes: {$all :[likes]}}).sort({birthdate:1}).limit(limit)
	else if(pais != "" and likes != "" and limit != "" and orden == "desc"):
		result = collection.find({'address.country': pais, likes: {$all :[likes]}}).sort({birthdate:-1}).limit(limit)
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
	querys = request.query_string #Obtenemos todos los campos de la URL
	querys2 = querys.split('&')

	for item in querys2:
		item = item.split('=')
		listaComparar.append(item[0])

	for item in listaComparar:
		if(item != 'month'):
			if(item == ''):
				 return '''<p> Campos vacios! </p>'''
			else:
			       	return '''<p>Has introducido mal el campo {{item}}</p>'''

	nacimiento = request.query.birthdate

	if(nacimiento != ""): #TODO
		result = collection.find({'birthdate.1':nacimiento[1]}).sort({birthdate.0:1,birthdate.1:1,birthdate.2:1})
	else:
		return '''<p>Error! Vacio</p>'''

	if result.count() > 0:
		output = template("output", Cursor = result, Elementos = result.count())
       		return output
	else:
		 return '''<p>No se han encontrado resultados</p>'''
