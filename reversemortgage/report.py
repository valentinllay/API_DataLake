import random


# reversemortgage.report_simplified
def build_report_simplified(inputs_simplified: dict) -> dict:
    """
    Construction de l'input complet à partir d'un input simplifié.
    Simplifie les resultats du calcul de LTV pour masquer tous les détails du calculateur.
    """
    real_estate_type = inputs_simplified["real_estate_type"]
    insee_code = inputs_simplified["insee_code"]

    # Construction de l'input complet
    data: dict = get_default_data()
    data["collateral_asset"]["real_estate_type"] = real_estate_type
    data["collateral_asset"]["insee_code"] = insee_code

    # Appel calcul ltv complet
    results: dict = build_report(data)

    # Construction de l'output simplifé
    ltv = results["Base Case"]["maximum_quotity"]
    prix_5p = results["Base Case"]["Quantile_Prix_Immo"]["prix 5%"]
    results_simplified: dict = {
        "ltv": ltv,
        "prix_5%": prix_5p
    }

    return results_simplified



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


# reversemortgage.report
def build_report(data, TAEG_parameters=None):
    """
    Simule le vrai build_report.
    """

    maximum_quotity: float = random.randint(1_000,6_000)/10_000
    prix_5p: int = random.randint(500_000, 1_500_000)

    results = {
        "Base Case": {
            "Quantile_Prix_Immo": {
                "prix 5%": None
            },
            "maximum_quotity": None
        }
    }
    results["Base Case"]["maximum_quotity"] = maximum_quotity
    results["Base Case"]["Quantile_Prix_Immo"]["prix 5%"] = prix_5p

    return results


if __name__ == "__main__":
    inputs_simplified = {
        "real_estate_type": 1,
        # "insee_code": "83130"
    }
    response_simplified = build_report_simplified(inputs_simplified)
    print(response_simplified)