#!/usr/bin/python3
from views import console
import subprocess
import new_pass_generator as new_pass_generator
import pass_regenerator as pass_regenerator

def mostrar_menu():
    while True:
        print('\033[92m' + "************************************************************************************************" + '\033[0m')
        print(f'\033[1mBienvenido al gestor de pases\033[0m')
        print("1. Generar nuevo pase (cambia serial_number y auth_token).")
        print("2. Modificar un pase existente y mandar notificacion a servidores de apple.")
        print("3. Mandar fichero pkpass por correo.")
        print("4. Borrar una version de un pase.")
        print("5. Salir")
        print('\033[92m' + "************************************************************************************************" + '\033[0m')

        opcion = input("Seleccione una opción (1-5): ")
        
        if opcion == "1":
            # Realizar acción para la opción 1
            print("Ha seleccionado la opción 1")
            new_pass_generator.main()
        elif opcion == "2":
            # Realizar acción para la opción 2
            ruta_absoluta_al_pkpass = pass_regenerator.main()
            # if ruta_absoluta_al_pkpass == "" or ruta_absoluta_al_pkpass is None:
            #     raise Exception("ruta_absoluta_al_pkpass is empty")
        elif opcion == "3":
            # Realizar acción para la opción 5
            print("Ha seleccionado la opción 3")
            subprocess.run(['python3', "./utils/emailSender.py"])
        elif opcion == "4":
            # Salir del programa
            print("Ha seleccionado la opción 4")
            subprocess.run(['python3', "./utils/delete_pass.py"])
        elif opcion == "5":
            # Salir del programa
            print("Saliendo del programa...")
            break
        else:
            print("Opción inválida. Por favor, seleccione un número del 1 al 4.")

# Llamar a la función para mostrar el menú
try:
    mostrar_menu()
except Exception as e:
    print(f"An error occurred: {str(e)}")