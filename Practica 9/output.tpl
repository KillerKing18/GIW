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
<h1>CONSULTA 1</h1>
</head>
<body>

	<table>
                <tr>
                       <th>Pais</th>
                       <th>Numero de usuarios</th>
                </tr>
   
	%count = 0
	%for elem in Cursor:
		%count = count + 1
		<tr>
		<th style="font-weight:normal;">{{elem['_id']}}</th>
		<th style="font-weight:normal;" >{{elem['count']}}</th>
		<tr>	
	%end	
	</table>
<h2>Numero de elementos encontrados = {{count}}</h2>
</body>
</html>
