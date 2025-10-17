import json
import random
import re
from phanterpwa.tools import (
    checkbox_bool,
    string_escape
)
from .autorizacao import turma_eh_educacao_infantil
from decimal import Decimal
from datetime import (
    date,
    timedelta,
    datetime
)

re_data = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}")

def muda_nome(nome_completo):
    nome = nome_completo.split(" ")
    nomes = [
        "Marte",
        "Vênus",
        "Júpiter",
        "Netuno",
        "Mercurio",
        "Saturno",
        "Urano"
        "Ceres",
        "Loki",
        "Thor",
        "Hulk",
        "Zeus",
        "Hera",
        "Prometeus",
        "Jazão",
        "Aquiles",
        "Brizeis",
        "Apollo",
        "Éris",
        "Poseidon",
        "Juno",
        "Minerva",
        "Vesta",
        "Vulcano",
        "Ártemis",
        "Héstia",
        "Hermes",
        "Deméter",
        "Eros",
        "Afrodite",
        "Cronos",
        "Hefesto",
        "Ares",
        "Ilítia"
    ]
    escolha = random.choice(nomes)
    if len(nome) > 2:
        return "{0} {1}".format(escolha, " ".join(nome[-2:]))
    else:
        return "{0} da Grécia".format(escolha)