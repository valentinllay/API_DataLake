# -*- coding: utf-8 -*-
"""
Created on Fri Jul 11 11:01:52 2025

@author: ValentinLeLay

validators.py
"""

from errors.exceptions import InputValidationError


def validate_greeting_payload(data: dict) -> dict[str, str | None]:
    """
    Vérifie la présence et le type (str ou None) des clés 'genre', 'prenom', 'nom' dans le JSON.

    Raises:
        InputValidationError: si une clé est présente mais n’est pas une chaîne.
    """
    genre: str|None = data.get("genre", None)
    prenom: str|None = data.get("prenom", None)
    nom: str|None = data.get("nom", None)

    for key, val in (("genre", genre), ("prenom", prenom), ("nom", nom)):
        if val is not None and not isinstance(val, str):
            raise InputValidationError(f"'{key}' doit être une chaîne ou absent, reçu : {val!r}")

    return {"genre": genre, "prenom": prenom, "nom": nom}


def validate_ltv_request_data(data: dict) -> tuple[str, int, str]:
    """
    Valide les champs 'insee_code', 'age', 'borrower' dans un body JSON.
    Lève une InputValidationError si un champ est manquant ou invalide.

    Returns:
        tuple (insee_code, age (int), borrower)
    """
    insee_code = data.get('insee_code')
    age_raw = data.get('age')
    borrower = data.get('borrower')

    if not insee_code or not borrower or age_raw is None:
        raise InputValidationError("Paramètres requis : insee_code, age, borrower")

    try:
        age = int(age_raw)
    except (ValueError, TypeError):
        raise InputValidationError(f"age doit être un entier, reçu : {age_raw!r}")

    return insee_code, age, borrower
