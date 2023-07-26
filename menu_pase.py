#!/usr/bin/python3
from views import console
import subprocess
import new_pass_generator as new_pass_generator
import pass_regenerator as pass_regenerator
import pass_updater as pass_updater

def mostrar_menu():
    while True:
        print('\033[92m' + "************************************************************************************************" + '\033[0m')
        print(f'\033[1mBienvenido al gestor de pases\033[0m')
        print("1. Generar nuevo pase (cambia serial_number y auth_token).")
        print("2. Modificar un pase existente y mandar notificacion a servidores de apple.")
        print("3. Actualizar un pase existente.")
        print("4. Mandar fichero pkpass por correo.")
        print("5. Borrar una version de un pase.")
        print("6. Salir")
        print('\033[92m' + "************************************************************************************************" + '\033[0m')

        opcion = input("Seleccione una opción (1-6): ")
        
        if opcion == "1":
            print(f'\033[92m\nHa seleccionado generar nuevo pase. \033[0m')
            new_pass_generator.main()
        elif opcion == "2":
            print(f'\033[92m\nHa seleccionado modificar un pase existente. \033[0m')
            pass_regenerator.main()
            #ruta_absoluta_al_pkpass = pass_regenerator.main()
            # if ruta_absoluta_al_pkpass == "" or ruta_absoluta_al_pkpass is None:
            #     raise Exception("ruta_absoluta_al_pkpass is empty")
        elif opcion == "3":
            print(f'\033[92m\nHa seleccionado actualizar un pase existente. \033[0m')
            pass_updater.main()
        elif opcion == "4":
            print(f'\033[92m\n Ha seleccionado mandar un pase por email. \033[0m')
            subprocess.run(['python3', "./utils/emailSender.py"])
        elif opcion == "5":
            print(f'\033[92m\n Ha seleccionado eliminar un pase. \033[0m')
            subprocess.run(['python3', "./utils/delete_pass.py"])
        elif opcion == "6":
            # Salir del programa
            print("Saliendo del programa...")
            break
        else:
            print("Opción inválida. Por favor, seleccione un número del 1 al 6.")

# Llamar a la función para mostrar el menú
try:
    mostrar_menu()
except Exception as e:
    print(f"An error occurred: {str(e)}")