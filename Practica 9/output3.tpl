<!--
Carlos Bilbao, Mario Bocos, Álvaro López y David Élbez declaramos que esta solución es fruto exclusivamente
de nuestro trabajo personal. No hemos sido ayudados por ninguna otra persona ni hemos
obtenido la solución de fuentes externas, y tampoco hemos compartido nuestra solución
con nadie. Declaramos además que no hemos realizado de manera deshonesta ninguna otra
actividad que pueda mejorar nuestros resultados ni perjudicar los resultados de los demás.
-->
<!DOCTYPE html>
<html>
<head>
<h1>CONSULTA</h1>
</head>
<body>

	<table>
                <tr>
                       <th>Nombre del pais</th>
                       <th>Rango</th>
					   <th>Edad minima</th>
                       <th>Edad maxima</th>
                </tr>
   
	%count = 0
	%for elem in Cursor:
		%count = count + 1
		<tr>
		<th style="font-weight:normal;">{{elem['_id']}}</th>
		<th style="font-weight:normal;" >{{elem['rango']}}</th>
		<th style="font-weight:normal;" >{{elem['edad_minima']}}</th>
		<th style="font-weight:normal;" >{{elem['edad_maxima']}}</th>
		<tr>
	%end	
	</table>
<h2>Numero de elementos encontrados = {{count}}</h2>
</body>
</html>