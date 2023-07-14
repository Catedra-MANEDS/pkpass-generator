#!/usr/bin/python3
import os
import shutil
import hashlib
import json
import subprocess
import psycopg2
import glob 
from typing import Callable, Optional, TypedDict
import string_generator
from pass_object import pass_object
from zipfile import ZipFile

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
    directorio_pass_seleccionado=menu_directorios_pass(DIRECTORIO_CON_LOS_PUNTO_PASS)
    directorio_del_nuevo_pase=nuevo_directorio_pase(directorio_pass_seleccionado)
    if directorio_del_nuevo_pase == "" or directorio_del_nuevo_pase is None :
         raise Exception("directorio_del_nuevo_pase is empty")
    
    FOLDER_PUNTO_PASS=directorio_del_nuevo_pase
    ruta_nuevo_pass_json=os.path.join(directorio_del_nuevo_pase, "pass.json")

    pass_object_new_auth_and_serial(ruta_nuevo_pass_json)

    #Creamos manifest
    ruta_manifest=create_manifest_json(asset_path=FOLDER_PUNTO_PASS)

    #Creamos signature y la ruta donde guardarlo
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
    shutil.move(f"{PKPASS_NAME}.pkpass", DIRECTORIO_CON_LOS_PKPASS)

def connect_to_bd():
    con = psycopg2.connect(
    database="passData",
    user="samuel",
    password="hola",
    host="34.175.112.41",
    port= '5432'
    )
    return con

def menu_directorios_pass(directorio_a_mostrar):

    directorios = [archivo for archivo in os.listdir(directorio_a_mostrar) if archivo.endswith('.pass')]
    print("\nMenú de directorios plantilla:")
    for i, archivo in enumerate(directorios, start=1):
        print(f"\t{i}. {archivo}")

    # Leer la selección del usuario
    opcion = input("\nSeleccione el número de la plantilla a usar: ")

    # Validar la entrada del usuario
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

def nuevo_directorio_pase(directorio_pass_plantilla):
    #Asignamos a la variable global PKPASS_NAME, el nombre que tendra el pkpass final
    global PKPASS_NAME 
    PKPASS_NAME = input("Introduzca el nombre del nuevo pkpass: ")
    ruta_directorio_nuevo_pase=os.path.join(DIRECTORIO_CON_LOS_PUNTO_PASS, f"{PKPASS_NAME}.pass")
    # Comprobar si el directorio ya existe
    if os.path.exists(ruta_directorio_nuevo_pase):
        print("Un directorio de pase con ese nombre ya existe. Introduzca un nombre válido.")
        return nuevo_directorio_pase(directorio_pass_plantilla)
    else:
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
    print("\nArchivo generado: manifest.json.")
    print("\tY almacenado en el directorio .pass")

    return f"{asset_path}/manifest.json"

def pass_object_new_auth_and_serial(ruta_archivo_json):

    auth_token = string_generator.generar_cadena_aleatoria(33)
    #Guardamos en la bd el auth_token generado
    # con=connect_to_bd()
    # cursor = con.cursor()
    # insert_sql="INSERT INTO authentication(authenticationtoken) VALUES(%s)"
    # values=(auth_token,)
    # cursor.execute(insert_sql,values)
    # con.commit()
    # cursor.close()
    # con.close()

    serial_number = string_generator.generar_cadena_numeros_aleatorios(10)
    with open(ruta_archivo_json, "r") as f:
        contenido_json = json.load(f)

    contenido_json["authenticationToken"] = auth_token
    contenido_json["serialNumber"] = serial_number

    #pass_object_json = json.dumps(contenido_json, indent=2)
    with open(ruta_archivo_json, "w") as f:
        json.dump(contenido_json, f, indent=2)

    print("\nCambios en auth_token y serial_number guardados en el pass.json.")

if __name__ == '__main__':
    main()