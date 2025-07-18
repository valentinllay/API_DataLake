# -*- coding: utf-8 -*-
"""
Created on Fri Jul 11 11:01:52 2025

@author: ValentinLeLay

validators.py
"""

from errors.exceptions import InputValidationError


def validate_insee_code(raw_code: str | int) -> str:
    """
    Valide et normalise un code INSEE en chaîne de 5 chiffres.

    Args:
        raw_code: code INSEE initial, sous forme d'entier ou de chaîne.
    Returns:
        Le code INSEE formaté sur 5 chiffres (avec un zéro en tête si nécessaire).
    Raises:
        InputValidationError: si le résultat n'est pas une chaîne de 5 chiffres.
    """
    code_str = str(raw_code).zfill(5)
    if not (code_str.isdigit() and len(code_str) == 5):
        raise InputValidationError(
            f"Le code INSEE doit être un entier de 5 chiffres, reçu : {raw_code}"
        )
    return code_str


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


def validate_maximum_quotity_payload(data: dict) -> dict[str, int | str | None]:
    """
    Valide le payload pour l'endpoint maximum_quotity.

    Raises:
        InputValidationError: si un champ requis est manquant ou de type incorrect.

    Returns:
        dict contenant age_1, gender_1, borrower_type, insee_code, real_estate_type,
        et éventuellement age_2, gender_2.
    """
    # Champs requis
    required_str = ["borrower_type", "insee_code"]
    required_int = ["age_1", "gender_1", "real_estate_type"]
    optional_int = ["age_2", "gender_2"]

    # Vérification présence et type
    for field in required_str:
        val = data.get(field)
        if not val or not isinstance(val, str):
            raise InputValidationError(f"'{field}' est requis et doit être une chaîne, reçu : {val!r}")
    for field in required_int:
        val = data.get(field)
        if val is None:
            raise InputValidationError(f"'{field}' est requis et doit être un entier")
        try:
            data[field] = int(val)
        except (TypeError, ValueError):
            raise InputValidationError(f"'{field}' doit être convertible en entier, reçu : {val!r}")

    # Champs optionnels
    for field in optional_int:
        val = data.get(field)
        if val is not None:
            try:
                data[field] = int(val)
            except (TypeError, ValueError):
                raise InputValidationError(f"'{field}' doit être convertible en entier ou absent, reçu : {val!r}")
        else:
            data[field] = None

    # Normalisation du code INSEE
    data["insee_code"] = validate_insee_code(data["insee_code"])

    return {
        "age_1": data["age_1"],
        "gender_1": data["gender_1"],
        "age_2": data["age_2"],
        "gender_2": data["gender_2"],
        "borrower_type": data["borrower_type"],
        "insee_code": data["insee_code"],
        "real_estate_type": data["real_estate_type"],
    }