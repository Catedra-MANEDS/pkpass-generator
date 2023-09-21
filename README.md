# pkpass-generator

Lógica del generador y actualizador de pases para apple wallet (ficheros .pkpass) 

## Estructura del proyecto
Se cuenta con 3 scripts principales que automatoizan la lógica necesaria para crear nuevos pases y modificar sus características, además de generar notificaciones PUSH. Adicionalmente, se cuenta con scripts que realizan funcionanes auxiliares. Por otro lado, se cuenta con los directorios donde se almacenan las plantillas de creación de pases. En estas plantillas se incluyen los archivos empleados en la creación de los pases, como las imagenes o fichero JSON que compondrán el pase. También se cuenta con un directorio donde se almacenan los certificados con los que se firman los pases, así como el directorio donde se almacenan los pases creados en su formato .pkpass. 

## Tabla de Contenidos

- [auto_new_pass_generator](#auto_new_pass_generator)
- [auto_new_pass_fields_regenerator](#auto_new_pass_fields_regenerator)
- [auto_pass_regenerator](#auto_pass_regenerator)
- [directorios_auxiliares](#directorios_auxiliares)

## auto_new_pass_generator

Script que automatiza la generación de un pase


## auto_new_pass_fields_regenerator

Script que actualiza un pase ya existente, para las notificaciones de contratos
 
## auto_pass_regenerator

Script que actualiza un pase ya existente, para las notificaciones de las campañas 
	

## directorios_auxiliares

	- directorios_punto_pass --> contiene las plantillas para la creación de pases
   	- pkpass_files --> contienen los pases en creados en formato .pkpass
   	- certificados --> contiene los certificados empleados para firmar los pases
   	- models --> contiene el modelo de datos para conectar con la base de datos
   	- utils --> contiene los scripts auxiliares
  





 


