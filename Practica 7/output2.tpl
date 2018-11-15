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
