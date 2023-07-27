import json
import os

def cargar_datos(ruta_archivo_json):
    with open(ruta_archivo_json, "r") as file:
        return json.load(file)

def guardar_datos(datos, ruta_archivo_json):
    with open(ruta_archivo_json, "w") as file:
        json.dump(datos, file, indent=2)

def obtener_keys_con_change_message(datos):
    keys = []
    for field in datos["eventTicket"]["secondaryFields"] + datos["eventTicket"]["backFields"] + datos["eventTicket"]["auxiliaryFields"]:
        if field.get("changeMessage"):
            keys.append(field["key"])
    return keys

def modificar_valor(datos, key, nuevo_valor):
    fields_to_search = datos["eventTicket"]["secondaryFields"] + datos["eventTicket"]["backFields"] + datos["eventTicket"]["auxiliaryFields"]
    
    for field in fields_to_search:
        if field.get("key") == key and field.get("changeMessage"):
            field["value"] = nuevo_valor
            break
    else:
        print(f"No se encontró el campo '{key}' con 'changeMessage' asociado.")

def main(directorio_pass_seleccionado):

    #Creamos la ruta al archivo pass.json
    ruta_archivo_json=os.path.join(directorio_pass_seleccionado, "pass.json")

    datos = cargar_datos(ruta_archivo_json)

    keys_con_change_message = obtener_keys_con_change_message(datos)
    
    while True:
        print("\nCampos con 'changeMessage' asociado:")
        for i, key in enumerate(keys_con_change_message, start=1):
            for field in datos["eventTicket"]["secondaryFields"] + datos["eventTicket"]["backFields"] + datos["eventTicket"]["auxiliaryFields"]:
                if field.get("key") == key:
                    print(f"\t{i}. 'key': '{key.ljust(15)}' ------ 'value': '{field.get('value')}'")
                    break

        opcion = input("Seleccione el número del campo que desea modificar (o 'q' para salir): ")

        if opcion == "q":
            break

        try:
            seleccion = int(opcion)
            if 1 <= seleccion <= len(keys_con_change_message):
                key = keys_con_change_message[seleccion - 1]
                nuevo_valor = str(input(f"Ingrese el nuevo valor para '{key}': "))
                modificar_valor(datos, key, nuevo_valor)
                guardar_datos(datos, ruta_archivo_json)
                print("Valor modificado con éxito.")
            else:
                print("Selección inválida. Por favor, elija un número válido.")
        except ValueError:
            print("Entrada inválida. Por favor, ingrese un número.")

    print("Saliendo del programa.")

if __name__ == "__main__":
    main()

# contenido_json["eventTicket"]["backFields"][-1]["value"] = nuevo_valor_image_change
# contenido_json["auxiliaryFields"][0]["value"] = nuevo_valor_oferta_principal