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
<h2>Numero de elementos encontrados = {{Elementos}}</h2>
</head>
<body>

	<table>
                <tr>
                       <th>Nombre de usuario </th>
                       <th>E-mail</th>
                       <th>Página web </th>
                       <th>Tarjeta de crédito </th>
                       <th>Hash de contraseña </th>
                       <th>Nombre </th>
                       <th>Apellido </th>
                       <th>Dirección </th> 
                       <th>Aficiones </th>
                       <th>Fecha de nacimiento</th>
                </tr>
   

	%for elem in Cursor:
	      <tr>
	      <th style="font-weight:normal;">{{elem['_id']}}</p></th>
              <th style="font-weight:normal;" >{{elem['email']}}</th> 
              <th style="font-weight:normal;" >{{elem['webpage']}}</th> 
              <th style="font-weight:normal;" >{{elem['credit_card']['number']}},{{elem['credit_card']['expire']['month']}},{{elem['credit_card']['expire']['year']}}</th> 
              <th style="font-weight:normal;" >{{elem['password']}} </th>
              <th style="font-weight:normal;" >{{elem['name']}}</th>
              <th style="font-weight:normal;">{{elem['surname']}}</th>
              <th style="font-weight:normal;">{{elem['address']['country']}},{{elem['address']['street']}},{{elem['address']['num']}},{{elem['address']['zip']}}</th> 
              <th style="font-weight:normal;" >{{elem['likes']}}</th>
              <th style="font-weight:normal;" >{{elem['birthdate']}}</th>
	      <tr>	
	%end	
	</table>
</body>
</html>
