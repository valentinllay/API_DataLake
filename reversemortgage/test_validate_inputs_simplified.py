# -*- coding: utf-8 -*-
"""
Created on Tue Jul  1 10:19:54 2025

@author: ValentinLeLay
"""

# test_validate_inputs.py

from reversemortgage.report_simplified import validate_inputs
from reversemortgage.report_simplified import InputValidationError

def run_test(name, inp, should_pass):
    try:
        validate_inputs(inp.copy())
        passed = True
    except InputValidationError as e:
        passed = False
        error = str(e)
    except Exception as e:
        passed = False
        error = f"Unexpected exception: {e}"
    status = "PASS" if passed == should_pass else "FAIL"
    msg = "" if passed else f" → {error}"
    print(f"{status}: {name}{msg}")

def main():
    tests = [
        ("Valid one borrower", {
            "real_estate_type": 1,
            "insee_code": "1234",
            "gender_1": "Homme",
            "age_1": 60,
            "gender_2": "",
            "age_2": ""
        }, True),

        ("Valid two borrowers", {
            "real_estate_type": "2",
            "insee_code": "01234",
            "gender_1": "Femme",
            "age_1": "65",
            "gender_2": "Homme",
            "age_2": "70"
        }, True),

        ("Valid type 'appartement'", {
            "real_estate_type": "appartement",
            "insee_code": "1234",
            "gender_1": "Homme",
            "age_1": 60,
            "gender_2": "",
            "age_2": ""
        }, True),

        ("Valid type 'maison'", {
            "real_estate_type": "Maison",
            "insee_code": "1234",
            "gender_1": "Homme",
            "age_1": 60,
            "gender_2": "",
            "age_2": ""
        }, True),

        ("Missing real_estate_type", {
            "insee_code": "1234",
            "gender_1": "Homme",
            "age_1": 60
        }, False),

        ("Empty insee_code", {
            "real_estate_type": 1,
            "insee_code": "",
            "gender_1": "Homme",
            "age_1": 60
        }, False),

        ("Invalid real_estate_type", {
            "real_estate_type": 3,
            "insee_code": "1234",
            "gender_1": "Homme",
            "age_1": 60
        }, False),

        ("Invalid insee_code length", {
            "real_estate_type": 1,
            "insee_code": "123",
            "gender_1": "Homme",
            "age_1": 60
        }, False),

        ("Invalid gender_1", {
            "real_estate_type": 1,
            "insee_code": "1234",
            "gender_1": "Autre",
            "age_1": 60
        }, False),

        ("Non-int age_1", {
            "real_estate_type": 1,
            "insee_code": "1234",
            "gender_1": "Homme",
            "age_1": "abc"
        }, False),

        ("Age_1 out of range", {
            "real_estate_type": 1,
            "insee_code": "1234",
            "gender_1": "Homme",
            "age_1": 59
        }, False),

        ("One field only for second borrower", {
            "real_estate_type": 1,
            "insee_code": "1234",
            "gender_1": "Homme",
            "age_1": 60,
            "gender_2": "Femme",
            "age_2": ""
        }, False),

        ("Insee code non-digit", {
            "real_estate_type": 1,
            "insee_code": "12A34",
            "gender_1": "Homme",
            "age_1": 60
        }, False),

        ("Real estate type non-entier (string)", {
            "real_estate_type": "X",
            "insee_code": "1234",
            "gender_1": "Homme",
            "age_1": 60
        }, False),

        ("Age_1 hors limite haute", {
            "real_estate_type": 1,
            "insee_code": "1234",
            "gender_1": "Homme",
            "age_1": 123
        }, False),

        ("Pas de keys optional (absence totale)", {
            "real_estate_type": 1,
            "insee_code": "1234",
            "gender_1": "Homme",
            "age_1": 60
        }, True),

        ("Optional None explicite", {
            "real_estate_type": 1,
            "insee_code": "1234",
            "gender_1": "Homme",
            "age_1": 60,
            "gender_2": None,
            "age_2": None
        }, True),

        ("Second age non-numerique", {
            "real_estate_type": 1,
            "insee_code": "1234",
            "gender_1": "Homme",
            "age_1": 60,
            "gender_2": "Femme",
            "age_2": "abc"
        }, False),

        ("Second age hors limite basse", {
            "real_estate_type": 1,
            "insee_code": "1234",
            "gender_1": "Homme",
            "age_1": 60,
            "gender_2": "Femme",
            "age_2": 59
        }, False),

        ("Insee code trop long (6 chiffres)", {
            "real_estate_type": 1,
            "insee_code": "123456",
            "gender_1": "Homme",
            "age_1": 60
        }, False),
    ]

    for name, inp, should_pass in tests:
        run_test(name, inp, should_pass)

if __name__ == "__main__":
    main()
