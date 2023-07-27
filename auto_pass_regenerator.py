#!/usr/bin/python3
import os
import shutil
import json
import requests
import sys
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

    if len(sys.argv) < 4:
        print("Usage: python3 path_auto_new_pass_regenerator.py <message> <nombre>")
        sys.exit(1)

    # Obtener los argumentos de entrada pasados al script
    campaing_message = sys.argv[1]
    nombre = sys.argv[2]
    campaign_id = int(sys.argv[3])

    directorio_pass_seleccionado=os.path.join(globals.DIRECTORIO_CON_LOS_PUNTO_PASS , f"{nombre}.pass")
    ruta_nuevo_directorio=generar_directorio_copia(directorio_pass_seleccionado)
    if ruta_nuevo_directorio == "" or ruta_nuevo_directorio is None :
        raise Exception("ruta_nuevo_directorio is empty")
        
    ruta_archivo_json=os.path.join(ruta_nuevo_directorio, "pass.json")
    print("\nRuta al json")
    print(ruta_archivo_json)
    modificar_oferta(ruta_archivo_json,campaing_message)

    #Almacenamos la ruta al directorio .pass _new
    FOLDER_PUNTO_PASS= os.path.abspath(ruta_nuevo_directorio)
    ruta_directorio_new=FOLDER_PUNTO_PASS

    ruta_directorio_original=extraer_cliente(nombre,campaign_id)
    if ruta_directorio_original == "" or ruta_directorio_original is None :
         raise Exception("directorio_del_nuevo_pase is empty")
    
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

    #Obtenemos rutas absolutas a los pkpass new y original
    ruta_absoluta_al_pkpass_new = os.path.join(ruta_directorio_pkpass, f"{PKPASS_NAME}.pkpass")
    ruta_absoluta_al_pkpass_original = os.path.join(ruta_directorio_pkpass, f"{nombre}.pkpass")
    """
     ruta_directorio_original --> extraido de la tablaclientes
     FOLDER_PUNTO_PASS --> ruta al directorio copia _new
     ruta_absoluta_al_pkpass_new --> creados con os.path.abspath + os.path.join + nombre _new
     ruta_absoluta_al_pkpass_original creados con os.path.abspath + os.path.join + nombre original -->
    """
    print("\n\nRutas inicio")
    print(ruta_directorio_original)
    print(ruta_absoluta_al_pkpass_original)
    print(ruta_directorio_new)
    print(ruta_absoluta_al_pkpass_new)
    # Eliminar el directorio original y renombrar el directorio FOLDER_PUNTO_PASS
    if os.path.exists(ruta_directorio_original):
        shutil.rmtree(ruta_directorio_original)
        print(f"Se ha elimnado el directorio:{ruta_directorio_original}")
        os.rename(ruta_directorio_new, ruta_directorio_original)  # Renombrar directorio FOLDER_PUNTO_PASS

    # Eliminar el archivo original y renombrar el archivo nuevo
    if os.path.exists(ruta_absoluta_al_pkpass_original):
        os.remove(ruta_absoluta_al_pkpass_original)  # Eliminar archivo original
        print(f"Se ha elimnado el fichero:{ruta_directorio_original}")
        os.rename(ruta_absoluta_al_pkpass_new, ruta_absoluta_al_pkpass_original)  # Renombrar archivo nuevo

    print("\n\nRutas fin")
    print(ruta_directorio_original)
    print(ruta_absoluta_al_pkpass_original)
    print(ruta_directorio_new)
    print(ruta_absoluta_al_pkpass_new)
    #Actualizamos datos del pase en la bd
    save_pass_data_to_db(ruta_directorio_original,ruta_absoluta_al_pkpass_original,nombre)

    # """Generamos una solicitud """
    url_base = "https://pepephone.jumpingcrab.com:5000"
    respuesta_server=common_functions.notify_apple_devices(url_base,pass_type_identifier,serial_number)
    print(f"\n{respuesta_server}")

    # Si todo se ejecuto bien, salir con código de retorno 0 (éxito)
    sys.exit(0)

"""-----------------------------------FUNCIONES AUXILIARES-------------------------------------------"""
def modificar_oferta(ruta_archivo_json,campaing_message):
        
    # Leer el archivo JSON
    with open(ruta_archivo_json, 'r') as archivo:
        contenido_json = json.load(archivo)

    contenido_json["eventTicket"]["auxiliaryFields"][0]["value"] = campaing_message

    # Guardar los cambios en el archivo JSON

    with open(ruta_archivo_json, 'w') as archivo:
        json.dump(contenido_json, archivo, indent=4)

    print("\nFichero json modificado con éxito.")

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

# def generar_directorio_copia(directorio):
#     global PKPASS_NAME

#     # Separamos el nombre y la extensión .pass del directorio
#     nombre_directorio, extension = os.path.splitext(directorio)
#     numero_inicial = 1

#     # Comprobamos si el nombre tiene patrón _new_X, (siendo X un número)
#     patron = r"_new_\d+$"
#     coincidencia = re.search(patron, nombre_directorio)

#     # Si lo tiene, cambiamos número X por X+1
#     if coincidencia:
#         numero_detectado = int(coincidencia.group()[5:])
#         nuevo_numero = numero_detectado + 1
#         nombre_nuevo_directorio = re.sub(patron, f"_new_{nuevo_numero}", nombre_directorio)
#     else:
#         # Si no lo tiene, nombramos _new_1
#         nombre_nuevo_directorio = f"{nombre_directorio}_new_{numero_inicial}"

#     PKPASS_NAME = os.path.basename(nombre_nuevo_directorio)
#     nombre_nuevo_directorio = os.path.abspath(nombre_nuevo_directorio)  # Obtenemos la ruta completa del directorio

#     # Comprobar si el nuevo directorio ya existe, si existe se incrementa el número
#     while os.path.exists(nombre_nuevo_directorio):
#         numero_inicial += 1
#         nombre_nuevo_directorio = f"{nombre_directorio}_new_{numero_inicial}"
#         PKPASS_NAME = os.path.basename(nombre_nuevo_directorio)
#         nombre_nuevo_directorio = os.path.abspath(nombre_nuevo_directorio)

#     # Crear el nuevo directorio
#     os.mkdir(nombre_nuevo_directorio)

#     print("\nDirectorio creado:", nombre_nuevo_directorio)

#     evitar_archivos = [
#         "signature",
#         "manifest.json",
#     ]

#     # Copiar los archivos del directorio original al nuevo directorio
#     archivos = os.listdir(directorio)
#     for archivo in archivos:
#         if archivo not in evitar_archivos:
#             ruta_origen = os.path.join(directorio, archivo)
#             if not os.path.samefile(ruta_origen, nombre_nuevo_directorio):
#                 shutil.copy2(ruta_origen, nombre_nuevo_directorio)

#     return nombre_nuevo_directorio

def save_pass_data_to_db(ruta_nuevo_directorio,ruta_absoluta_al_pkpass,nombre):

    print("\nRUTA PA GUARDAR EN LA DB")
    print(ruta_absoluta_al_pkpass)
    #La variable serial_number será accedida desde main 
    global serial_number, pass_type_identifier
    ruta_archivo_json=os.path.join(ruta_nuevo_directorio, "pass.json")
    Session = sessionmaker(bind=engine)
    session = Session()

    with open(ruta_archivo_json, "r") as f:
        contenido_json = json.load(f)

    serial_number= contenido_json["serialNumber"] 
    pass_type_identifier=contenido_json["passTypeIdentifier"] 

    #Convertimos diccionario json a una cadena JSON para guardarlo en la base de datos
    passDataJson = json.dumps(contenido_json)

    # Formatear el timestamp como cadena de texto en el formato 'YYYY-MM-DD HH:MM:SS'
    timestamp_actual = datetime.now()
    timestamp_actual = timestamp_actual.strftime('%Y-%m-%d %H:%M:%S')

    passes_to_update = session.query(Passes).filter(
    (Passes.serialnumber == serial_number) & (Passes.passtypeidentifier == pass_type_identifier)).first()
    if passes_to_update:
    # Actualizar los atributos passdata y updatetimestamp con los valores deseados
        passes_to_update.passdatajson = passDataJson
        passes_to_update.updatetimestamp = timestamp_actual
        passes_to_update.pkpass_name = f"{nombre}.pkpass"
        passes_to_update.pkpass_route = ruta_absoluta_al_pkpass
    # Confirmar los cambios realizados en la sesión
        session.commit()
    session.close()
    print("\nPase actualizado en la base de datos. ")

def extraer_cliente(nombre,campaign_id):

    Session = sessionmaker(bind=engine)
    session = Session()

    # Realizar la consulta para obtener "ruta_directorio_pass"
    cliente = session.query(Clientes).filter_by(nombre=nombre, campaign_id=campaign_id).first()
    session.close()

    if cliente:
        ruta_directorio_cliente = cliente.ruta_directorio_pass
        print(f"\nRuta del directorio del cliente: {ruta_directorio_cliente}")
        return ruta_directorio_cliente
    else:
        print("No se encontró un cliente con el nombre y Campaign ID especificados.")
        return None

if __name__ == '__main__':
    """El main de pass_regenerator retorna la ruta al pkpass modificado"""
    ruta_absoluta_al_pkpass=main()

