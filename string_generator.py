#!/usr/bin/python3

import random
import string

def generar_cadena_aleatoria(longitud):
    caracteres = string.ascii_letters + string.digits
    cadena_aleatoria = ''.join(random.choice(caracteres) for _ in range(longitud))
    return cadena_aleatoria

def generar_cadena_numeros_aleatorios(longitud):
    cadena = ""
    for _ in range(longitud):
        digito = random.randint(0, 9)  # Genera un número aleatorio entre 0 y 9
        cadena += str(digito)
    return cadena


if __name__ == '__main__':
    cadena_aleatoria=generar_cadena_aleatoria()
    print(cadena_aleatoria)
