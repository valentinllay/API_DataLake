import reversemortgage.report


class InputValidationError(Exception):
    """
    Erreur levée quand les inputs sont invalides.
    Sert à distinguer une erreur lié à l'intput user d'une erreur interne de calcul de LTV.
    """
    pass


def validate_inputs(data: dict) -> None:
    """
    Valide et normalise :
     - real_estate_type doit exister, être convertible en int, et valoir 1 ou 2
     - insee_code doit exister, être 4 ou 5 chiffres ; on pad à 5 chiffres
    Lève InputValidationError si un contrôle échoue.
    """
    # 1) Présence et non-empty
    for field in ("real_estate_type", "insee_code"):
        if field not in data:
            raise InputValidationError(f"Le parametre '{field}' est requis")
        value = data[field]
        # Excel envoie "" pour une cellule vide : on le traite comme manquant
        if value is None or (isinstance(value, str) and value.strip() == ""):
            raise InputValidationError(f"Le parametre '{field}' ne peut pas etre vide")

    # 2) real_estate_type
    try:
        val = int(data["real_estate_type"])
    except (TypeError, ValueError):
        raise InputValidationError("real_estate_type doit etre un entier et doit valoir 1 (appart) ou 2 (maison)")
    if val not in (1, 2):
        raise InputValidationError("real_estate_type doit valoir 1 (appart) ou 2 (maison)")
    data["real_estate_type"] = val

    # 3) insee_code
    code = str(data["insee_code"])
    if not code.isdigit() or not (4 <= len(code) <= 5):
        raise InputValidationError("insee_code doit etre un nombre de 4 ou 5 chiffres")
    # padding à 5 chiffres
    data["insee_code"] = f"{int(code):05d}"


def build_report(inputs: dict) -> dict:
    """
    Construction de l'input complet à partir d'un input simplifié.
    Simplifie les résultats du calcul de LTV pour masquer tous les détails du calculateur.
    """
    validate_inputs(inputs)

    real_estate_type = inputs["real_estate_type"]
    insee_code = inputs["insee_code"]

    # construction de l'input complet
    data = get_default_data()
    data["collateral_asset"]["real_estate_type"] = real_estate_type
    data["collateral_asset"]["insee_code"] = insee_code

    # calcul LTV complet
    results = reversemortgage.report.build_report(data)

    # sortie simplifiée
    return {
        "ltv":     results["Base Case"]["maximum_quotity"],
        "prix_5%": results["Base Case"]["Quantile_Prix_Immo"]["prix 5%"]
    }


def get_default_data():
    """
    Inputs par défaut.
    """
    data = {
      "calculation_parameters": {
        "calculation_date": "2025-06-10",
        "calculation_mode": 1,
        "expected_loss_to_fail_scenario": 0,
        "annual_time_steps": 1,
        "projection_years": 60,
        "mortality_diversification": True,
        "global_scenarios": [
          0
        ],
        "loss_quantile_to_use": -1,
        "discount_losses": True,
        "verbose": True,
        "pricing_method": "advanced"
      },
      "borrowers": [
        {
          "birth_date": "1949-02-27",
          "gender": 1,
          "income_quantile": 11,
          "alive": True
        }
      ],
      "collateral_asset": {
        "real_estate_type": None, # A CHANGER
        "last_price_estimation_date": "2024-10-10",
        "last_price_estimation": 220000,
        "insee_code": None, # A CHANGER
        "type_bien": "Résidence principale"
      },
      "loan_terms": {
        "already_issued": False,
        "issue_date": "2099-01-01",
        "initial_outstanding": 1,
        "grace_period": 0.25,
        "levier_taux_variable": 0,
        "quotity": None,
        "bank": "ARRAGO"
      },
      "liability_financing": {
        "already_issued": False,
        "issue_date": "2099-01-01",
        "levier_taux_variable": 0,
        "initial_outstanding": 0
      }
    }

    return data



if __name__ == "__main__":
    inputs = {
        "real_estate_type": "1",
        "insee_code": "83130"
    }
    response_simplified = build_report(inputs)
    print(response_simplified)