#!/usr/bin/python3
from models.db_model import *
from datetime import datetime
import json
import os
import shutil
import time
from utils import constants as globals
from utils import common_functions as common_functions
from utils import change_value_json as change_value_json

def main():
    """Para evitar que se creen copias de carpetas si no se va a modificar nada, primero se pregunta"""
    directorio_pass_seleccionado=common_functions.menu_directorios_pass(globals.DIRECTORIO_CON_LOS_PUNTO_PASS)
    copiar_y_renombrar_directorio(directorio_pass_seleccionado,globals.DIRECTORIO_CON_LOS_PUNTO_PASS)

    #Separamos el nombre y la extesion .pass del directorio
    partes = directorio_pass_seleccionado.split("/")
    PKPASS_NAME = partes[-1].split(".")[0]

    change_value_json.main(directorio_pass_seleccionado)

    #Almacenamos la ruta al directorio .pass
    FOLDER_PUNTO_PASS=directorio_pass_seleccionado

    #Creamos manifest
    ruta_manifest=common_functions.create_manifest_json(ruta_directorio_pass=FOLDER_PUNTO_PASS)

    #Create signature y la ruta donde almacenar signature
    ruta_signature=os.path.join(FOLDER_PUNTO_PASS, "signature")
    common_functions.generar_signature(ruta_manifest,ruta_signature)

    #Creamos el fichero .pkpass comprimiendo todos los ficheros del directorio .pass
    common_functions.generate_pkpass(FOLDER_PUNTO_PASS,PKPASS_NAME)

    ruta_destino=os.path.join(globals.DIRECTORIO_CON_LOS_PKPASS, f"{PKPASS_NAME}.pkpass")
    #Si hay que sobreescribir el archivo, shutil.move no funciona, usamos replace
    if os.path.exists(ruta_destino):
        os.replace(f"{PKPASS_NAME}.pkpass", ruta_destino)
    else:
        shutil.move(f"{PKPASS_NAME}.pkpass", ruta_destino)
        
    # ruta_directorio_pkpass = os.path.abspath(globals.DIRECTORIO_CON_LOS_PKPASS)
    # ruta_absoluta_al_pkpass = os.path.join(ruta_directorio_pkpass, f"{PKPASS_NAME}.pkpass")
    ruta_absoluta_al_pkpass = os.path.abspath(ruta_destino)

    #Actualizamos datos del pase en la bd
    save_pass_data_to_db(directorio_pass_seleccionado,ruta_absoluta_al_pkpass,PKPASS_NAME)

    # """Generamos una solicitud """
    url_base = "https://pepephone.jumpingcrab.com:5000"
    respuesta_server=common_functions.notify_apple_devices(url_base,pass_type_identifier,serial_number)
    print(f"\n{respuesta_server}")


def save_pass_data_to_db(ruta_nuevo_directorio,ruta_absoluta_al_pkpass,PKPASS_NAME):

    #La variable serial_number será accedida desde main 
    global serial_number, pass_type_identifier
    ruta_archivo_json=os.path.join(ruta_nuevo_directorio, "pass.json")
    Session = sessionmaker(bind=engine)
    session = Session()

    with open(ruta_archivo_json, "r") as f:
        contenido_json = json.load(f)

    serial_number= contenido_json["serialNumber"] 
    pass_type_identifier=contenido_json["passTypeIdentifier"] 
    # Formatear el timestamp como cadena de texto en el formato 'YYYY-MM-DD HH:MM:SS'
    timestamp_actual = datetime.now()
    timestamp_actual = timestamp_actual.strftime('%Y-%m-%d %H:%M:%S')
    #Convertimos diccionario json a una cadena JSON para guardarlo en la base de datos
    passDataJson = json.dumps(contenido_json)

    passes_to_update = session.query(Passes).filter(
    (Passes.serialnumber == serial_number) & (Passes.passtypeidentifier == pass_type_identifier)).first()
    if passes_to_update:
    # Actualizar los atributos passdata y updatetimestamp con los valores deseados
        passes_to_update.passdatajson = passDataJson
        passes_to_update.updatetimestamp = timestamp_actual
        passes_to_update.pkpass_name = f"{PKPASS_NAME}.pkpass"
        passes_to_update.pkpass_route = ruta_absoluta_al_pkpass
    # Confirmar los cambios realizados en la sesión
        session.commit()
    session.close()
    print("\nPase actualizado en la base de datos. ")


def copiar_y_renombrar_directorio(ruta_original, directorio_destino):
    # Verificar que la ruta original exista
    if not os.path.exists(ruta_original):
        print(f"Error: El directorio {ruta_original} no existe.")
        return

    try:
        os.mkdir(os.path.join(directorio_destino, "copia.pass"))
        # Crear una copia del directorio en la ruta de destino
    except FileExistsError:
        print("Error: El directorio de destino ya existe.")
        return

    evitar_archivos = [
        "signature",
        "manifest.json",
    ]

    # Copiar los archivos del directorio original al nuevo directorio
    archivos = os.listdir(ruta_original)
    for archivo in archivos:
        if archivo not in evitar_archivos:
            ruta_origen = os.path.join(ruta_original, archivo)
            ruta_destino = os.path.join(directorio_destino, "copia.pass")
            if not os.path.samefile(ruta_origen, ruta_destino):
                shutil.copy2(ruta_origen, ruta_destino)


    # Renombrar el directorio copia al nombre del directorio original
    try:
        os.rename(ruta_original,os.path.join(directorio_destino, "basura.pass"))
        # Eliminar el directorio original
        eliminar_directorio_recursivo(os.path.join(directorio_destino, "basura.pass"))
        os.rename(os.path.join(directorio_destino, "copia.pass"), os.path.basename(ruta_original))
        print("Directorio copia renombrado correctamente.")
    except OSError as e:
        print(f"Error al renombrar el directorio copia: {e}")
        return
    
def eliminar_directorio_recursivo(ruta_directorio):
    for root, _, archivos in os.walk(ruta_directorio, topdown=False):
        for archivo in archivos:
            ruta_archivo = os.path.join(root, archivo)
            os.remove(ruta_archivo)
        os.rmdir(root)