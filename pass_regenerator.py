#!/usr/bin/python3
import os
import shutil
import hashlib
import json
import sys
from pass_object import pass_object
from zipfile import ZipFile
import modify_json as modify_json
import change_images as change_images
import time
import re
from db_model import *
from datetime import datetime

FOLDER_PUNTO_PASS = ""
PKPASS_NAME=""
OPENSSL_APP = "openssl"
DIRECTORIO_CON_LOS_PUNTO_PASS = "./directorios_punto_pass"
DIRECTORIO_CON_LOS_PKPASS="./pkpass_files/"

SUPPORTED_ASSET_FILES = [
    "icon.png",
    "icon@2x.png",
    "background.png",
    "background@2x.png",
    "logo.png",
    "logo@2x.png",
    "footer.png",
    "footer@2x.png",
    "strip.png",
    "strip@2x.png",
    "thumbnail.png",
    "thumbnail@2x.png",
    "signature",
    "pass.json",
    "manifest.json",
]

"""Creamos las rutas a los certificados"""
#directorio_certificados="/home/samuel/pass_generator/certificados/"
directorio_certificados="/home/samuel/Documents/pkpassApple/pkpassPepephone/scp_mandar/certificados/"
#Certificado de apple
certificado_apple=directorio_certificados+"AppleWWDRCA.pem"
#Certificado del pase
pkpass_pem=directorio_certificados+"pkpass.pem"
#Clave del pase
pass_pem=directorio_certificados+"pass.pem"
#Contraseña
key_password = "pepe"
certificate_password="pepe"
pass_type_identifier="pass.com.pepephone.eventTicket"

def main():
    """Para evitar que se creen copias de carpetas si no se va a modificar nada, primero se pregunta"""
    """MODIFICAR EL imagenes del pase escogido"""
    que_modificar="imágenes"
    respuesta_image = preguntar_modificacion(que_modificar)
    """MODIFICAR EL pass.json del pase escogido"""
    que_modificar="pass.json"
    respuesta_pass = preguntar_modificacion(que_modificar)

    if respuesta_pass == "s" or respuesta_image == "s":

        directorio_pass_seleccionado=menu_directorios_pass(DIRECTORIO_CON_LOS_PUNTO_PASS)
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

    save_pass_data_to_db()
    #Almacenamos la ruta al directorio .pass
    FOLDER_PUNTO_PASS=ruta_nuevo_directorio

    ruta_manifest=create_manifest_json(asset_path=FOLDER_PUNTO_PASS)

    #Create signature y la ruta donde almacenar signature
    ruta_signature=os.path.join(FOLDER_PUNTO_PASS, "signature")
    os_code = os.system(f"{OPENSSL_APP} smime -binary -sign -certfile {certificado_apple} -signer {pass_pem} -inkey {pkpass_pem} -in {ruta_manifest} -out {ruta_signature} -outform DER -passin pass:{key_password}")
    if os_code != 0:
        raise Exception("could not create signature")
    print("\nArchivo generado: signature.")

    asset_files = []
    for (_, _, filenames) in os.walk(f"{FOLDER_PUNTO_PASS}"):
        for filename in filenames:
            if filename in SUPPORTED_ASSET_FILES:
                shutil.copy2(f"{FOLDER_PUNTO_PASS}/{filename}", filename)
                asset_files.append(filename)

    with ZipFile(f"{PKPASS_NAME}.pkpass", "w") as zip_file:
        for asset_file in asset_files:
            zip_file.write(asset_file)

    #Eliminamos los ficheros del directorio actual usados para crear el zip
    print("\nEliminacion de archivos residuales...")
    for file_name in asset_files:
        file_path = os.path.join(os.getcwd(), file_name)
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"Archivo eliminado: {file_name}.")
        else:
            print(f"El archivo no existe: {file_name}.")

    print("\nArchivo Pkpass generado existosamente.")

    ruta_destino=os.path.join(DIRECTORIO_CON_LOS_PKPASS, f"{PKPASS_NAME}.pkpass")
    #Si hay que sobreescribir el archivo, shutil.move no funciona, usamos replace
    if os.path.exists(ruta_destino):
        os.replace(f"{PKPASS_NAME}.pkpass", ruta_destino)
    else:
        shutil.move(f"{PKPASS_NAME}.pkpass", ruta_destino)
    ruta_al_directorio_de_pases = os.path.abspath(DIRECTORIO_CON_LOS_PKPASS)
    ruta_absoluta_al_pkpass = os.path.join(ruta_al_directorio_de_pases, f"{PKPASS_NAME}.pkpass")
    return ruta_absoluta_al_pkpass

def preguntar_modificacion(que_modificar):
    respuesta = ""
    while respuesta != "s" and respuesta != "n":
        respuesta = input(f'\033[92m\n¿Desea modificar {que_modificar}? (s/n): \033[0m')
        respuesta = respuesta.lower()
        if respuesta != "s" and respuesta != "n":
            print("respuesta_image inválida. Intente nuevamente.")
    return respuesta

def create_manifest_json(asset_path: str):
    with open(f"{asset_path}/pass.json", "r") as f:
        pass_json = f.read()

    hashed_pass_json = hashlib.sha1(pass_json.encode('utf-8')).hexdigest()

    manifest_dict = {"pass.json": hashed_pass_json}

    for (_, _, filenames) in os.walk(asset_path):
        for filename in filenames:
            if filename in SUPPORTED_ASSET_FILES:
                manifest_dict[filename] = hashlib.sha1(
                    open(f"{asset_path}/{filename}", "rb").read()
                ).hexdigest()

    with open(f"{asset_path}/manifest.json", "w") as f:
        f.write(json.dumps(manifest_dict, indent=4))
    print("\nArchivo generado: manifest.json. ---> almacenado en el directorio .pass")

    return f"{asset_path}/manifest.json"

def menu_directorios_pass(directorio_a_mostrar):

    directorios = [archivo for archivo in os.listdir(directorio_a_mostrar) if archivo.endswith('.pass')]
    print("\nMenú de directorios .pass:")
    for i, archivo in enumerate(directorios, start=1):
        print(f"\t{i}. {archivo}")

    # Leer la selección del usuario
    opcion = input("\nSeleccione el número del pase a \033[1mMODIFICAR\033[0m: ")
    while not opcion.isdigit() or int(opcion) < 1 or int(opcion) > len(directorios):
        print("Selección inválida. Intente nuevamente.")
        opcion = input("Seleccione el número del archivo: ")

    # Obtener el archivo seleccionado
    directorio_seleccionado = directorios[int(opcion) - 1]
    ruta_directorio_seleccionado = os.path.join(directorio_a_mostrar, directorio_seleccionado)

    # Realizar las acciones deseadas con el archivo seleccionado
    print("\nDirectorio .pass seleccionado:", ruta_directorio_seleccionado)
    print()
    return ruta_directorio_seleccionado

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
            ruta_archivo_final = os.path.join(nombre_nuevo_directorio, archivo)
            print(f"La ruta destino es--> {ruta_destino}")
            print(f"La ruta_archivo_final es--> {ruta_archivo_final}")
            if not os.path.samefile(ruta_origen, ruta_destino):
                shutil.copy2(ruta_origen, ruta_destino)

    """QUEDA EL ERROR 
        SOLUCIONADO ---> DE QUE SI SON EXACTAMENTE LOS MISMOS ARCHIVOS LOS COPIA, regenerar pepito_new.pass 
        NO SOLUCIONADO ---> si no son los mismos archivos, ej hacer copia de un .pass sin version new, si da error
                        porque coge la ruta del directorio+archivo, y tiene que ser solo la del directorio
    """
    return nombre_nuevo_directorio

def save_pass_data_to_db(ruta_nuevo_pass_json):

    Session = sessionmaker(bind=engine)
    session = Session()

    with open(ruta_nuevo_pass_json, "r") as f:
        contenido_json = json.load(f)

    auth_token=contenido_json["authenticationToken"]
    serial_number= contenido_json["serialNumber"] 
    pass_type_identifier=contenido_json["passTypeIdentifier"] 
    # Formatear el timestamp como cadena de texto en el formato 'YYYY-MM-DD HH:MM:SS'
    timestamp_actual = datetime.now()
    timestamp_actual=timestamp_actual.strftime('%d-%m-%Y %H:%M:%S')

    #Añadimos los datos del nuevo pase y el auth_token a la bd
    new_pass = Passes(passtypeidentifier=pass_type_identifier,serialnumber=serial_number,updatetimestamp=timestamp_actual,passdatajson=contenido_json)
    session.add(new_pass)
    session.commit()
    session.close()
    print("\n Pase actualizado en la base de datos. ")


if __name__ == '__main__':
    """El main de pass_regenerator retorna la ruta al pkpass modificado"""
    ruta_absoluta_al_pkpass=main()
