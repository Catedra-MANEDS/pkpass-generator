#!/usr/bin/python3
from views import console
import subprocess
import pass_regenerator as pass_regenerator
import new_pass_generator as new_pass_generator

def mostrar_menu():
    while True:
        print('\033[92m' + "************************************************************************************************" + '\033[0m')
        print("Bienvenido al gestor de pases")
        print("1. Generar nuevo pase (cambia serial_number y auth_token).")
        print("2. Modificar un pase existente y mandar notificacion a servidores de apple.")
        print("3. Mandar fichero pkpass por correo.")
        print("4. Salir")
        print('\033[92m' + "************************************************************************************************" + '\033[0m')

        opcion = input("Seleccione una opción (1-4): ")
        
        if opcion == "1":
            # Realizar acción para la opción 1
            print("Ha seleccionado la opción 1")
            new_pass_generator.main()
        elif opcion == "2":
            # Realizar acción para la opción 2
            ruta_absoluta_al_pkpass = pass_regenerator.main()
            if ruta_absoluta_al_pkpass == "" or ruta_absoluta_al_pkpass is None:
                raise Exception("ruta_absoluta_al_pkpass is empty")
        elif opcion == "3":
            # Realizar acción para la opción 5
            print("Ha seleccionado la opción 3")
            subprocess.run(['python3', "emailSender.py"])
        elif opcion == "4":
            # Salir del programa
            print("Saliendo del programa...")
            break
        else:
            print("Opción inválida. Por favor, seleccione un número del 1 al 4.")

# Llamar a la función para mostrar el menú
mostrar_menu()