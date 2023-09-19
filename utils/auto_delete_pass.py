#!/usr/bin/python3
import os
import json
import sys
import re #para expresiones regulares
#from db_model import *
ruta_directorio_padre = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(ruta_directorio_padre)

def eliminar_pase(ruta_directorio):
    
                ruta_directorio_punto_pass = ruta_directorio
                # Eliminar el directorio y su contenido
                eliminar_directorio_recursivo(ruta_directorio_punto_pass)
                print(f"\n{ruta_directorio_punto_pass} y su contenido han sido eliminados.")

                # Encontrar el archivo correspondiente con una extensión diferente en otro directorio
                ruta_directorio_correspondiente = "./pkpass_files"  
                archivo_correspondiente = os.path.splitext(ruta_directorio_punto_pass)[0] + ".pkpass"  
                
                ruta_archivo_correspondiente = os.path.join(ruta_directorio_correspondiente, archivo_correspondiente)
                if os.path.exists(ruta_archivo_correspondiente):
                    os.remove(ruta_archivo_correspondiente)
                    print(f"\n{archivo_correspondiente} ha sido eliminado del directorio de pkpass.")
                else:
                    print(f"\n{archivo_correspondiente} no existe en el directorio de pkpass.")


def eliminar_directorio_recursivo(ruta_directorio):
    for root, _, archivos in os.walk(ruta_directorio, topdown=False):
        for archivo in archivos:
            ruta_archivo = os.path.join(root, archivo)
            os.remove(ruta_archivo)
        os.rmdir(root)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Uso: python3 tu_script.py <ruta_directorio>")
        sys.exit(1)

    ruta_directorio = sys.argv[1]
    eliminar_pase(ruta_directorio)
