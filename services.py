# -*- coding: utf-8 -*-
"""
Created on Fri Jul 11 11:01:52 2025

@author: ValentinLeLay

services.py
Logique métier de l’API : composition d’appels repository,
transformation des résultats en structures Python.
"""

from repository import fetch_latest_calcul_ltv
from errors.exceptions import NotFoundError
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


def get_latest_ltv(insee_code: str, age: int, borrower: str) -> dict | None:
    """
    Renvoie un dict représentant la dernière entrée de LTV,
    ou None si aucun résultat n’a été trouvé.
    """
    row = fetch_latest_calcul_ltv(insee_code, age, borrower)
    if row is None:
        raise NotFoundError(f"Aucun calcul LTV trouvé pour insee_code={insee_code}, age={age}, borrower={borrower}")
    return dict(row)
