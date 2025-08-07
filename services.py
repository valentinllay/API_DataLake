# -*- coding: utf-8 -*-
"""
Created on Fri Jul 11 11:01:52 2025

@author: ValentinLeLay

services.py
Logique métier de l’API : composition d’appels repository,
transformation des résultats en structures Python.
"""

from repository import fetch_maximum_quotity
from hello_world.greet import say_hello_world, personalized_greeting


def get_generic_greeting() -> str:
    """
    Renvoie la salutation générique.
    """
    return say_hello_world()


def get_personalized_greeting(genre: str | None, prenom: str | None, nom: str | None) -> str:
    """
    Renvoie la salutation personnalisée.
    """
    return personalized_greeting(genre, prenom, nom)


def get_maximum_quotity(
    age_1: int,
    gender_1: int,
    age_2: int | None,
    gender_2: int | None,
    borrower_type: str,
    insee_code: str,
    real_estate_type: str,
) -> float:
    """
    Ordonne la récupération de maximum_quotity et gère l'absence de résultat.
    Si la simulation existe et que maximum_quotity est Null alors c'est inéligible donc
    la LTV doit-être de zéro.
    """
    mq: float|None = fetch_maximum_quotity(
        age_1, gender_1, borrower_type,
        insee_code, real_estate_type,
        age_2, gender_2
    )
    # Inéligbilité
    if mq is None:
        mq = 0.0
    return mq
