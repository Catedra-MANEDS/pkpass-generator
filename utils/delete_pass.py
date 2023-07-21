#!/usr/bin/python3
import os
import json
import sys
import re #para expresiones regulares
#from db_model import *
ruta_directorio_padre = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(ruta_directorio_padre)
from config_db.db_model import *

def eliminar_directorio_seleccionado_y_archivo_correspondiente(ruta_directorio):
    # Obtener una lista de directorios en el directorio especificado
    directorios = [directorio for directorio in os.listdir(ruta_directorio) if os.path.isdir(os.path.join(ruta_directorio, directorio))]
    
    if not directorios:
        print("No se encontraron directorios en el directorio especificado.")
        return

    print("Directorios disponibles en el directorio:")
    for i, nombre_directorio in enumerate(directorios, start=1):
        print(f"\t{i}. {nombre_directorio}")

    while True:
        try:
            # Pedir al usuario que seleccione un directorio por su número
            seleccion = int(input("Seleccione el número del directorio a eliminar: "))
            
            if 1 <= seleccion <= len(directorios):
                directorio_seleccionado = directorios[seleccion - 1]
                ruta_directorio_seleccionado = os.path.join(ruta_directorio, directorio_seleccionado)
                #Si es directorio tipo _new_X, actualizamos el pase a la ruta del directorio base
                if acaba_en_new_x_pass:
                    actualizar_pase_en_bd(ruta_directorio_seleccionado)
                 #Si NO es directorio tipo _new_X, será un directorio base y se elimina de la bd
                else:
                    #Eliminar el pase de la bd
                    eliminar_pase_en_bd(ruta_directorio_seleccionado)
                # Eliminar el directorio seleccionado y su contenido
                eliminar_directorio_recursivo(ruta_directorio_seleccionado)
                print(f"\n{directorio_seleccionado} y su contenido han sido eliminados.")

                # Encontrar el archivo correspondiente con una extensión diferente en otro directorio
                ruta_directorio_correspondiente = "./pkpass_files"  
                archivo_correspondiente = os.path.splitext(directorio_seleccionado)[0] + ".pkpass"  
                
                ruta_archivo_correspondiente = os.path.join(ruta_directorio_correspondiente, archivo_correspondiente)
                if os.path.exists(ruta_archivo_correspondiente):
                    os.remove(ruta_archivo_correspondiente)
                    print(f"\n{archivo_correspondiente} ha sido eliminado del directorio de pkpass.")
                else:
                    print(f"{archivo_correspondiente} no existe en el directorio de pkpass.")
                break
            else:
                print("Selección inválida. Por favor, elija un número válido.")
        except ValueError:
            print("Entrada inválida. Por favor, ingrese un número.")

def eliminar_directorio_recursivo(ruta_directorio):
    for root, _, archivos in os.walk(ruta_directorio, topdown=False):
        for archivo in archivos:
            ruta_archivo = os.path.join(root, archivo)
            os.remove(ruta_archivo)
        os.rmdir(root)

def eliminar_pase_en_bd(ruta_directorio):

    session, pass_to_delete = extraer_pase_de_bd(ruta_directorio)
    if pass_to_delete:
        #Eliminar fila encontrada
        session.delete(pass_to_delete)
        # Confirmar los cambios realizados en la sesión
        session.commit()
    session.close()
    print("\nPase eliminado de la base de datos. ")

def actualizar_pase_en_bd(ruta_directorio):
    session, pass_to_update = extraer_pase_de_bd(ruta_directorio)
    if pass_to_update:
        #Actualizar ruta al pkpass
        directorio_base=directorio_sin_new_X(ruta_directorio)
        nombre_sin_directorio_padre = os.path.basename(directorio_base)
        nombre_sin_extension, _ = os.path.splitext(nombre_sin_directorio_padre)

        nombre_extension_pkpass = nombre_sin_extension + ".pkpass"
        ruta_al_pkpass="./pkpass_files/"+nombre_extension_pkpass
        ruta_absoluta_pkpass = os.path.abspath(ruta_al_pkpass)

        pass_to_update.pkpass_name=nombre_extension_pkpass
        pass_to_update.pkpass_route=ruta_absoluta_pkpass
        # Confirmar los cambios realizados en la sesión
        session.commit()
    session.close()
    print("\nRuta al pkpass actualizada en la base de datos. ")

def extraer_pase_de_bd(ruta_directorio):
    ruta_archivo_json=os.path.join(ruta_directorio, "pass.json")
    with open(ruta_archivo_json, "r") as f:
        contenido_json = json.load(f)

    serial_number= contenido_json["serialNumber"] 
    pass_type_identifier=contenido_json["passTypeIdentifier"] 

    #Establecemos conexion con la bd
    Session = sessionmaker(bind=engine)
    session = Session()

    pass_to_delete = session.query(Passes).filter(
    (Passes.serialnumber == serial_number) & (Passes.passtypeidentifier == pass_type_identifier)).first()
    
    return session,pass_to_delete

def acaba_en_new_x_pass(ruta_directorio):
    pattern = r"_new_\d+\.pass$"  # Regular expression pattern to match "_new_" followed by digits and ".pass" at the end
    return re.search(pattern, ruta_directorio) is not None  #retorna true o false

def directorio_sin_new_X(ruta_directorio):
    patron = r"_new_\d+"  #expresión regular para encontrar "_new_X", donde X representa uno o más dígitos
    return re.sub(patron, "", ruta_directorio)    # Reemplaza el patrón  con cadena vacía ("") 

# Ejemplo de uso:
directorio_pkpass="./directorios_punto_pass/"
eliminar_directorio_seleccionado_y_archivo_correspondiente(directorio_pkpass)

