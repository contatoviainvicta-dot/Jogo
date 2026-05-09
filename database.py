import json
import random


def carregar_casos():

    with open("casos.json", "r", encoding="utf-8") as arquivo:
        casos = json.load(arquivo)

    return casos


def obter_caso_aleatorio():

    casos = carregar_casos()

    return random.choice(casos)
