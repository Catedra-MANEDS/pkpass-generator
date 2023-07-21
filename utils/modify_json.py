#!/usr/bin/python3
import json
import os
import sys
import time

def modificar_valor_simple(json_data):
    clave = input("\nIngrese la clave a modificar: ")
    nuevo_valor = input("Ingrese el nuevo valor: ")
    print()
    json_data[clave] = str(nuevo_valor)

def modificar_valor_complejo(json_data):
    print("\nRecuerde el formato es:")
    print("\t\tjson_data['eventTicket']['secondaryFields'][0]['value'] = value")
    print("\t\teventTicket.secondaryFields.0.value")
    print("\t\tEmpezando por [0]...")
    clave = input("\n\tIngrese la clave a modificar: ")
    nuevo_valor = str(input("\tIngrese el nuevo valor: "))
    print()

    claves = clave.split('.')
    objeto_actual = json_data

    for key in claves[:-1]:
        if isinstance(objeto_actual, dict):
            objeto_actual = objeto_actual.get(key)
        elif isinstance(objeto_actual, list):
            index = int(key)
            if index < len(objeto_actual):
                objeto_actual = objeto_actual[index]
            else:
                raise IndexError(f"Index {index} is out of range for list")
        else:
            raise TypeError(f"Cannot access key '{key}' in object of type {type(objeto_actual).__name__}")

    if isinstance(objeto_actual, dict) or isinstance(objeto_actual, list):
        ultimo_key = claves[-1]
        objeto_actual[ultimo_key] = nuevo_valor
    else:
        raise TypeError(f"Cannot update value for key '{ultimo_key}' in object of type {type(objeto_actual).__name__}")


def preguntar_modificacion(json_data):
    # Solicitar al usuario si desea realizar modificaciones
    respuesta = input('\033[92m'+"¿Desea "+"\033[1mMODIFICAR\033[0m"+'\033[92m'+" alguna clave y valor? (s/n): "+'\033[0m')
    # Realizar modificaciones si el usuario lo solicita
    if respuesta.lower() == 's':
        while True:
            tipo_modificacion = input("\n\t¿Qué tipo de modificación desea realizar? (simple/compleja) --> (s/c): ")
            if tipo_modificacion.lower() == 's':
                modificar_valor_simple(json_data)
            elif tipo_modificacion.lower() == 'c':
                modificar_valor_complejo(json_data)

            respuesta = input('\033[92m'+"\n¿Desea realizar otra modificación? (s/n): "+'\033[0m')
            if respuesta.lower() == 'n':
                break


def mostrar_contenido_json(json_data, lineas_por_iteracion):
    #Parametrod e json.dumps() -->  sort_keys=True
    contenido_json = json.dumps(json_data, indent=4).splitlines()
    num_lineas = len(contenido_json)
    indice = 0
    print()
    while indice < num_lineas:
        limite_superior = min(indice + lineas_por_iteracion, num_lineas)
        for linea in contenido_json[indice:limite_superior]:
            print(linea)
        print()
        preguntar_modificacion(json_data)
        if limite_superior < num_lineas:
            respuesta = input('\033[92m'+"\n¿Deseas "+"\033[1mVER\033[0m"+'\033[92m'+" más líneas? (s/n): "+'\033[0m')
            if respuesta.lower() != "s":
                break

        indice += lineas_por_iteracion

def main(ruta_directorio_punto_pass):

    print(f'\033[33m\nA continuacion va a modificar pass.json...\033[0m')
    time.sleep(0.5)
    ruta_archivo_json=os.path.join(ruta_directorio_punto_pass, "pass.json")

    # Leer el archivo JSON
    with open(ruta_archivo_json, 'r') as archivo:
        contenido_json = json.load(archivo)
    
    # Mostrar el contenido JSON de forma legible y ordenada
    mostrar_contenido_json(contenido_json, 25)

    # Guardar los cambios en el archivo JSON
    with open(ruta_archivo_json, 'w') as archivo:
        json.dump(contenido_json, archivo, indent=4)

    print("\nFichero json modificado con éxito.")

if __name__ == '__main__':
    main()

 
