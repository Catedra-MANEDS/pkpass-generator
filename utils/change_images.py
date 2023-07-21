import os
import shutil
import time

def mostrar_menu(opciones):
    print("\nSeleccione una opción:")
    for i, opcion in enumerate(opciones, start=1):
        print(f"\t{i}. {opcion}")
    return input("Ingrese el número de la imagen a modificar: ")

def eliminar_imagen_residual(ruta_imagen_residual):
    try:
        os.remove(ruta_imagen_residual)
        print(f"\nArchivo {ruta_imagen_residual} eliminado con éxito.")
    except FileNotFoundError:
        print(f"\nEl archivo {ruta_imagen_residual} no existe.")

def modificar_strip_image(ruta_strip):
    imagenes = [f for f in os.listdir(ruta_strip) if f.endswith(".png")]
    opciones = imagenes + ["Cancelar"]

    while True:
        opcion = mostrar_menu(opciones)
        if opcion.isdigit() and 1 <= int(opcion) <= len(imagenes):
            imagen_seleccionada = imagenes[int(opcion) - 1]
            ruta_imagen_original = os.path.join(ruta_strip, imagen_seleccionada)
            nueva_ruta = os.path.join(ruta_strip, "strip@2x.png")
            shutil.copy(ruta_imagen_original, nueva_ruta)
            print(f"\nImagen {imagen_seleccionada} modificada y guardada como strip@2x.png")
            return nueva_ruta
        elif opcion == str(len(opciones)):
            print("Operación cancelada.")
            break
        else:
            print("Opción inválida. Intente nuevamente.")

def modificar_footer_image(ruta_footer):
    imagenes = [f for f in os.listdir(ruta_footer) if f.endswith(".png")]
    opciones = imagenes + ["Cancelar"]

    while True:
        opcion = mostrar_menu(opciones)
        if opcion.isdigit() and 1 <= int(opcion) <= len(imagenes):
            imagen_seleccionada = imagenes[int(opcion) - 1]
            ruta_imagen_original = os.path.join(ruta_footer, imagen_seleccionada)
            nueva_ruta = os.path.join(ruta_footer, "footer@2x.png")
            shutil.copy(ruta_imagen_original, nueva_ruta)
            print(f"\nImagen {imagen_seleccionada} modificada y guardada como footer@2x.png")
            return nueva_ruta
        elif opcion == str(len(opciones)):
            print("Operación cancelada.")
            break
        else:
            print("Opción inválida. Intente nuevamente.")

def obtener_imagenes_disponibles(ruta_directorio):
    # Obtener la lista de archivos en el directorio
    archivos = os.listdir(ruta_directorio)

    # Filtrar los archivos por extensión .png
    imagenes = [archivo for archivo in archivos if archivo.lower().endswith(".png")]

    return imagenes

def main(ruta_directorio_pass):
    
    print(f'\033[94m\nA continuacion va a modificar las imagenes del pase...\033[0m')
    time.sleep(0.5)
    ruta_strip = os.path.join(os.getcwd(), "strip_images")
    ruta_footer = os.path.join(os.getcwd(), "footer_images")

    while True:
        print(f'\033[92m\nMenú de opciones:\033[0m')
        print("\t1. Modificar strip_image")
        print("\t2. Modificar footer_image")
        print("\t0. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            ruta_nueva_imagen=modificar_strip_image(ruta_strip)
            shutil.copy2(ruta_nueva_imagen, ruta_directorio_pass)
            eliminar_imagen_residual(ruta_nueva_imagen)
        elif opcion == "2":
            ruta_nueva_imagen=modificar_footer_image(ruta_footer)
            shutil.copy2(ruta_nueva_imagen, ruta_directorio_pass)
            eliminar_imagen_residual(ruta_nueva_imagen)
        elif opcion == "0":
            break
        else:
            print("Opción inválida. Intente nuevamente.")

if __name__ == "__main__":
    main()
