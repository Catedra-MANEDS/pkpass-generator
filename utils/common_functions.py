import subprocess
import os
import hashlib
import json
import shutil
import requests
from zipfile import ZipFile
from utils import constants as globals

"""Fichero contenedor de funciones comunes a ambos scripts pass_regenerator y new_pass_generator"""

#---------------------------------------------------------------------------------------
#Funcion para mostrar directorios
def menu_directorios_pass(directorio_a_mostrar):

    directorios = [archivo for archivo in os.listdir(directorio_a_mostrar) if archivo.endswith('.pass')]
    print("\nMenú de directorios .pass:")
    for i, archivo in enumerate(directorios, start=1):
        print(f"\t{i}. {archivo}")

    # Leer la selección del usuario
    opcion = input("\nSeleccione el número del pase a \033[1mMODIFICAR\033[0m: ")
    
    while not opcion.isdigit() or int(opcion) < 1 or int(opcion) > len(directorios):
        print("Selección inválida. Intente nuevamente.")
        opcion = input("Seleccione el número del directorio: ")

    # Obtener el archivo seleccionado
    directorio_seleccionado = directorios[int(opcion) - 1]
    ruta_directorio_seleccionado = os.path.join(directorio_a_mostrar, directorio_seleccionado)

    # Realizar las acciones deseadas con el archivo seleccionado
    print("\nDirectorio .pass seleccionado:", ruta_directorio_seleccionado)
    print()
    return ruta_directorio_seleccionado

#---------------------------------------------------------------------------------------
#Funcion para generar el fichero manifest
def create_manifest_json(ruta_directorio_pass: str):
    with open(f"{ruta_directorio_pass}/pass.json", "r") as f:
        pass_json = f.read()

    hashed_pass_json = hashlib.sha1(pass_json.encode('utf-8')).hexdigest()

    manifest_dict = {"pass.json": hashed_pass_json}

    for (_, _, filenames) in os.walk(ruta_directorio_pass):
        for filename in filenames:
            if filename in globals.SUPPORTED_ASSET_FILES:
                manifest_dict[filename] = hashlib.sha1(
                    open(f"{ruta_directorio_pass}/{filename}", "rb").read()
                ).hexdigest()

    with open(f"{ruta_directorio_pass}/manifest.json", "w") as f:
        f.write(json.dumps(manifest_dict, indent=4))
    print("\nArchivo generado: manifest.json. ---> almacenado en el directorio .pass")

    return f"{ruta_directorio_pass}/manifest.json"

#---------------------------------------------------------------------------------------
#Funcion para generar la firma de los ficheros del pkpass, emplea --> certificado_apple, certificado_pase y clave
def generar_signature(ruta_manifest,ruta_signature):
    # Comando para firmar sin contraseña
    cmd_no_password = [
        globals.OPENSSL_APP,
        "smime",
        "-binary",
        "-sign",
        "-certfile", globals.certificado_apple,
        "-signer", globals.pass_certificate,
        "-inkey", globals.passkey,
        "-in", ruta_manifest,
        "-out", ruta_signature,
        "-outform", "DER"
    ]
    # Comando para firmar con contraseña
    cmd_with_password = cmd_no_password + ["-passin", f"pass:{globals.key_password}"]
    
    try:
        # Intentar ejecutar el comando sin contraseña
        result = subprocess.run(cmd_no_password, check=True, capture_output=True, text=True)
        if result.returncode == 0:
            print("\nFirma creada exitosamente (sin contraseña)")
        else:
            # Si se produce un error, significa que la clave requiere contraseña,
            # entonces intentar ejecutar el comando con contraseña
            result = subprocess.run(cmd_with_password, check=True)
            print("F\nirma creada exitosamente (con contraseña)")

    except subprocess.CalledProcessError as e:
        print("Error al firmar:", e)

    print("\nArchivo generado: signature.")

#---------------------------------------------------------------------------------------
#Funcion para generar el pkpass, comprimiendo en formato .pkpass todos los ficheros del directorio .pass
def generate_pkpass(FOLDER_PUNTO_PASS,PKPASS_NAME):

    asset_files = []
    for (_, _, filenames) in os.walk(f"{FOLDER_PUNTO_PASS}"):
        for filename in filenames:
            if filename in globals.SUPPORTED_ASSET_FILES:
                shutil.copy2(f"{FOLDER_PUNTO_PASS}/{filename}", filename)
                asset_files.append(filename)

    with ZipFile(f"{PKPASS_NAME}.pkpass", "w") as zip_file:
        for asset_file in asset_files:
            zip_file.write(asset_file)
    print(asset_files)

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

#---------------------------------------------------------------------------------------
#Funcion para notificar a apple de que se ha realizado un cambio en el pase
def notify_apple_devices(url_base,pass_type_identifier,serial_number):
    
    #Creamos la URL destino de la solicitud
    url = f"{url_base}/notify_apple_devices/{pass_type_identifier}/{serial_number}"
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