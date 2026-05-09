import json
import random


ARQUIVO_CASOS = "casos.json"


def carregar_casos():

    with open(ARQUIVO_CASOS, "r", encoding="utf-8") as arquivo:
        return json.load(arquivo)


def obter_caso_nao_repetido(casos_usados):

    casos = carregar_casos()

    casos_disponiveis = [
        caso for caso in casos
        if caso["id"] not in casos_usados
    ]

    if not casos_disponiveis:

        casos_usados.clear()

        casos_disponiveis = casos

    return random.choice(casos_disponiveis)


def embaralhar_diagnostico(diagnostico):

    letras = list(diagnostico.upper())

    random.shuffle(letras)

    return letras


def obter_cor_raridade(raridade):

    cores = {
        "Comum": "🟢",
        "Raro": "🔵",
        "Épico": "🟣",
        "Lendário": "🟠"
    }

    return cores.get(raridade, "⚪")
