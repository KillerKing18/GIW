<!DOCTYPE html>
<html>
 <head>
 	<title>{{titulo}}</title>
 	<meta charset="utf-8" />
 </head>
 <body>

	<a href = "/menu"> Retroceder </a>

	<h1></h1>
	<h3>Monumentos: </h3>

	<form action = "/display" method = "POST">
		<select name = "Monumentos" id = "mon">

		    %for museo in Lista:
		        <option value = {{museo}}> {{museo}}</option>
		    %end
		</select>

		<button type = "submit">Enviar</button> 
    </form>

 </body>
</html>