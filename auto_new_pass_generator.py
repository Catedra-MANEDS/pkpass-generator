#!/usr/bin/python3
import os
import shutil
import json
import sys
from datetime import datetime
from zipfile import ZipFile
from utils import string_generator
from utils import constants as globals
from utils import common_functions as common_functions
#from db_model import *
from models.db_model import *

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 auto_new_pass_generator.py <nombre>")
        sys.exit(1)

    # Obtener el argumento 'nombre'
    nombre = sys.argv[1]

    directorio_pass_seleccionado=os.path.join(globals.DIRECTORIO_CON_LOS_PUNTO_PASS , "plantilla.pass")
    directorio_del_nuevo_pase=nuevo_directorio_pase(directorio_pass_seleccionado,nombre)
    if directorio_del_nuevo_pase == "" or directorio_del_nuevo_pase is None :
         raise Exception("directorio_del_nuevo_pase is empty")
    
    FOLDER_PUNTO_PASS=directorio_del_nuevo_pase
    ruta_nuevo_pass_json=os.path.join(directorio_del_nuevo_pase, "pass.json")

    pass_object_new_auth_and_serial(ruta_nuevo_pass_json,nombre)

    #Creamos manifest
    ruta_manifest=common_functions.create_manifest_json(ruta_directorio_pass=FOLDER_PUNTO_PASS)

    #Creamos signature y la ruta donde guardarlo
    ruta_signature=os.path.join(FOLDER_PUNTO_PASS, "signature")
    common_functions.generar_signature(ruta_manifest,ruta_signature)

    #Creamos el fichero .pkpass comprimiendo todos los ficheros del directorio .pass
    common_functions.generate_pkpass(FOLDER_PUNTO_PASS,PKPASS_NAME)


    shutil.move(f"{PKPASS_NAME}.pkpass", globals.DIRECTORIO_CON_LOS_PKPASS)
    ruta_al_pkpass=os.path.join(globals.DIRECTORIO_CON_LOS_PKPASS, f"{PKPASS_NAME}.pkpass")
    save_pass_data_to_db(ruta_nuevo_pass_json,ruta_al_pkpass)

    # Si todo se ejecuto bien, salir con código de retorno 0 (éxito)
    sys.exit(0)

"""-----------------------------------FUNCIONES AUXILIARES-------------------------------------------"""
def nuevo_directorio_pase(directorio_pass_plantilla,nombre):
    #Asignamos a la variable global PKPASS_NAME, el nombre que tendra el pkpass final
    global PKPASS_NAME 
    PKPASS_NAME = nombre
    ruta_directorio_nuevo_pase=os.path.join(globals.DIRECTORIO_CON_LOS_PUNTO_PASS, f"{PKPASS_NAME}.pass")
    
    os.mkdir(ruta_directorio_nuevo_pase)
    print("\nDirectorio creado:", ruta_directorio_nuevo_pase)

    # Copiar archivos de la plantilla .pass al directorio recién creado
    directorio_origen = directorio_pass_plantilla
    directorio_destino = ruta_directorio_nuevo_pase
    archivos = os.listdir(directorio_origen)
    evitar_archivos = [
    "signature",
    "manifest.json",
    ]
    for archivo in archivos:
        if archivo not in evitar_archivos:
            ruta_origen = os.path.join(directorio_origen, archivo)
            ruta_destino = os.path.join(directorio_destino, archivo)
            shutil.copy2(ruta_origen, ruta_destino)
            
    return directorio_destino

def pass_object_new_auth_and_serial(ruta_archivo_json,nombre):

    with open(ruta_archivo_json, "r") as f:
        contenido_json = json.load(f)
    
    auth_token = string_generator.generar_cadena_aleatoria(33)
    serial_number = string_generator.generar_cadena_numeros_aleatorios(10)

    contenido_json["authenticationToken"] = auth_token
    contenido_json["serialNumber"] = serial_number
    contenido_json["eventTicket"]["headerFields"][0]["value"] = nombre

    #pass_object_json = json.dumps(contenido_json, indent=2)
    with open(ruta_archivo_json, "w") as f:
        json.dump(contenido_json, f, indent=2)

    print("\nCambios en auth_token, serial_number y titular guardados en el pass.json.")

def save_pass_data_to_db(ruta_nuevo_pass_json,ruta_al_pkpass):

    Session = sessionmaker(bind=engine)
    session = Session()

    with open(ruta_nuevo_pass_json, "r") as f:
        contenido_json = json.load(f)

    auth_token=contenido_json["authenticationToken"]
    serial_number= contenido_json["serialNumber"] 
    pass_type_identifier=contenido_json["passTypeIdentifier"] 
    # Formatear el timestamp como cadena de texto en el formato 'YYYY-MM-DD HH:MM:SS'
    timestamp_actual = datetime.now()
    timestamp_actual = timestamp_actual.strftime('%Y-%m-%d %H:%M:%S')
    #Convertimos diccionario json a una cadena JSON para guardarlo en la base de datos
    passDataJson = json.dumps(contenido_json)

    #Añadimos los datos del nuevo pase y el auth_token a la bd
    new_pass = Passes(passtypeidentifier=pass_type_identifier,serialnumber=serial_number,pkpass_name=f'{PKPASS_NAME}.pkpass',pkpass_route=ruta_al_pkpass,updatetimestamp=timestamp_actual,passdatajson=passDataJson)
    session.add(new_pass)
    session.commit()
    new_authentication = Authentication(authenticationtoken=auth_token,pkpass_name=f'{PKPASS_NAME}.pkpass')
    session.add(new_authentication)
    session.commit()
    session.close()
    print("\nPase guardado en la base de datos. ")

if __name__ == '__main__':
    main()