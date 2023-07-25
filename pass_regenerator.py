#!/usr/bin/python3
import os
import shutil
import json
import requests
import re   #module for regular expresions
from datetime import datetime
#import modify_json as modify_json
#import change_images as change_images
from utils import change_images as change_images
from utils import modify_json as modify_json
from utils import constants as globals
from utils import common_functions as common_functions
from models.db_model import *

def main():
    """Para evitar que se creen copias de carpetas si no se va a modificar nada, primero se pregunta"""

    """MODIFICAR EL imagenes del pase escogido"""
    que_modificar="imágenes"
    respuesta_image = preguntar_modificacion(que_modificar)
    """MODIFICAR EL pass.json del pase escogido"""
    que_modificar="pass.json"
    respuesta_pass = preguntar_modificacion(que_modificar)

    if respuesta_pass == "s" or respuesta_image == "s":

        directorio_pass_seleccionado=common_functions.menu_directorios_pass(globals.DIRECTORIO_CON_LOS_PUNTO_PASS)
        ruta_nuevo_directorio=generar_directorio_copia(directorio_pass_seleccionado)
        if ruta_nuevo_directorio == "" or ruta_nuevo_directorio is None :
            raise Exception("ruta_nuevo_directorio is empty")
        
    #Si NO se modifica imagen y tampoco pass.json
    else:
        print("\nNo ha realizado ninguna modificación al pase, finalizando programa.")
        #sys.exit()
        return   

    if respuesta_image == "s":
        change_images.main(ruta_nuevo_directorio)   
    if respuesta_pass == "s":
        modify_json.main(ruta_nuevo_directorio)

    #Almacenamos la ruta al directorio .pass
    FOLDER_PUNTO_PASS=ruta_nuevo_directorio

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
        
    ruta_directorio_pkpass = os.path.abspath(globals.DIRECTORIO_CON_LOS_PKPASS)
    ruta_absoluta_al_pkpass = os.path.join(ruta_directorio_pkpass, f"{PKPASS_NAME}.pkpass")

    #Actualizamos datos del pase en la bd
    save_pass_data_to_db(ruta_nuevo_directorio,ruta_absoluta_al_pkpass)

    # """Generamos una solicitud """
    url_base = "https://pepephone.jumpingcrab.com:5000"
    url = f"{url_base}/notify_apple_devices/{pass_type_identifier}/{serial_number}"
    respuesta_server=notify_apple_devices(url)
    print(f"\n{respuesta_server}")

    return ruta_absoluta_al_pkpass

"""-----------------------------------FUNCIONES AUXILIARES-------------------------------------------"""
def preguntar_modificacion(que_modificar):
    respuesta = ""
    while respuesta != "s" and respuesta != "n":
        respuesta = input(f'\033[92m\n¿Desea modificar {que_modificar}? (s/n): \033[0m')
        respuesta = respuesta.lower()
        if respuesta != "s" and respuesta != "n":
            print("respuesta_image inválida. Intente nuevamente.")
    return respuesta

def generar_directorio_copia(directorio):

    global PKPASS_NAME
    #Separamos el nombre y la extesion .pass del directorio
    nombre_directorio, extension = os.path.splitext(directorio)
    numero_inicial = 1
    #Comprobamos si el nombre tiene patron _new_X, (siendo X un numero)
    patron = r"_new_\d+$"
    coincidencia = re.search(patron, nombre_directorio)
    #Si lo tiene, cambiamos numero X por X+1
    if coincidencia:
        numero_detectado = int(coincidencia.group()[5:])
        nuevo_numero = numero_detectado+1
        nombre_nuevo_directorio = re.sub(patron, f"_new_{nuevo_numero}", nombre_directorio)
    #Si no lo tiene nombramos _new_1
    else:
        nombre_nuevo_directorio = f"{nombre_directorio}_new_{numero_inicial}"

    PKPASS_NAME = os.path.basename(nombre_nuevo_directorio)
    nombre_nuevo_directorio=nombre_nuevo_directorio+extension
    
    # Comprobar si el nuevo directorio ya existe, si existe se sobreescribe
    if os.path.exists(nombre_nuevo_directorio):
        print("\nEl directorio que quiere crear ya existe, será sobreescribido.")
        os.makedirs(nombre_nuevo_directorio, exist_ok=True)
    else:
        # Crear el nuevo directorio
        os.mkdir(nombre_nuevo_directorio)
    print("\nDirectorio creado:", nombre_nuevo_directorio)

    evitar_archivos = [
        "signature",
        "manifest.json",
        ]
    
    # Copiar los archivos del directorio original al nuevo directorio
    archivos = os.listdir(directorio)
    for archivo in archivos:
        if archivo not in evitar_archivos:
            ruta_origen = os.path.join(directorio, archivo)
            ruta_destino=nombre_nuevo_directorio
            #ruta_archivo_final = os.path.join(nombre_nuevo_directorio, archivo)
            if not os.path.samefile(ruta_origen, ruta_destino):
                shutil.copy2(ruta_origen, ruta_destino)

    """QUEDA EL ERROR 
        SOLUCIONADO ---> DE QUE SI SON EXACTAMENTE LOS MISMOS ARCHIVOS LOS COPIA, regenerar pepito_new.pass 
        NO SOLUCIONADO ---> si no son los mismos archivos, ej hacer copia de un .pass sin version new, si da error
                        porque coge la ruta del directorio+archivo, y tiene que ser solo la del directorio
    """
    return nombre_nuevo_directorio

def save_pass_data_to_db(ruta_nuevo_directorio,ruta_absoluta_al_pkpass):

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
    
def notify_apple_devices(url):
    try:
        response = requests.post(url)
        response.raise_for_status()  # Lanza una excepción si la respuesta tiene un código de error
        # Verificar si la respuesta está vacía
        if not response.text:
            print("La respuesta está vacía.")
            return None
        
        # Si el tipo de contenido es texto plano
        if 'text/plain' in response.headers.get('content-type', '').lower():
            return response.text
        
        # Si no es texto plano, asumir que es JSON
        else:
            return response.json()

    except requests.exceptions.RequestException as e:
        print(f"Error al realizar la llamada al endpoint: {e}")
        return f"Error al realizar la llamada al endpoint: {e}"

if __name__ == '__main__':
    """El main de pass_regenerator retorna la ruta al pkpass modificado"""
    ruta_absoluta_al_pkpass=main()

