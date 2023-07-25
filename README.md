# pkpass-generator

Generador y actualizador de pases para apple wallet (ficheros .pkpass) 

## Estructura del proyecto
Hay 3 scripts principales menu_pase,py, new_pass_generator.py y pass_regenerator.py, además de unos directorios auxiliares

## Tabla de Contenidos

- [menu_pase](#menu_pase)
- [new_pass_generator](#new_pass_generator)
- [pass_regenerator](#pass_regenerator)
- [directorios_auxiliares](#directorios_auxiliares)
- [Uso](#uso)

## menu_pase

Menu principal de todo el proyecto, muestra opciones como:

	-Crear un nuevo pase
	-Modificar y actualizar un pase existente 
	-Eliminar un pase
	-Enviar un pase por correo electronico

## new_pass_generator

Script que genera un nuevo pase.

	-Mediante un menú se escoge una plantilla para el nuevo pase a crear
	-Recoge por teclado el nombre para el nuevo pase
	
## pass_regenerator

Script que modifica y actualiza un pase ya existente.
	
	-Mediante un menú se escoge de los pases ya existentes cual se desea modificar

## directorios_auxiliares

- models --> contiene el modelo de tablas de la base de datos Postgress gestionada con SQLAlchemy
- utils -->

- pkpass_files --> directorio donde se almacenan los ficheros .pkpass generados
- directorios_punto_pass --> directorio con los directorios .pass que contienen los ficheros empleados para generar el fichero .pkpass
- footer_images --> directorio con footer_images adicionales para modificar las imagenes de un pase
- strip_images --> directorio con strip_images adicionales para modificar las imagenes de un pase






 

