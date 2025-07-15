# -*- coding: utf-8 -*-
"""
Created on Fri Jul 11 11:01:52 2025

@author: ValentinLeLay

services.py
Logique métier de l’API : composition d’appels repository,
transformation des résultats en structures Python.
"""

from repository import fetch_maximum_quotity
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

    Raises:
        NotFoundError: si aucun enregistrement ne correspond aux filtres.
    """
    mq = fetch_maximum_quotity(
        age_1, gender_1, borrower_type,
        insee_code, real_estate_type,
        age_2, gender_2
    )
    if mq is None:
        raise NotFoundError(
            f"Aucun maximum_quotity pour insee_code={insee_code}, "
            f"borrower_type={borrower_type}, ages=({age_1},{age_2}), "
            f"genders=({gender_1},{gender_2}), real_estate_type={real_estate_type}"
        )
    return mq
