import string
import random

def generador_codigo_partida():
    #Queremos retornar un código de 4 letras que identifique la partida
    lista_letras = list(string.ascii_uppercase)
    codigo_partida = random.choice(lista_letras) + random.choice(lista_letras) + random.choice(lista_letras) + random.choice(lista_letras)
    return codigo_partida