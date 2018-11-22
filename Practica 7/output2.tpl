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
<h1>CONSULTA 2</h1>
<h2>Numero de elementos encontrados = {{Elementos}}</h2>
</head>
<body>

	<table>
                <tr>
                       <th>Nombre de usuario </th>
                       <th>E-mail</th>
                       <th>Fecha de nacimiento</th>
                </tr>
   

	%for elem in Cursor:
	      <tr>
	      <th style="font-weight:normal;">{{elem['_id']}}</p></th>
              <th style="font-weight:normal;" >{{elem['email']}}</th> 
              <th style="font-weight:normal;" >{{elem['birthdate']}}</th>
	      <tr>	
	%end	
	</table>
</body>
</html>
