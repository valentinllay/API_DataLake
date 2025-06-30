# -*- coding: utf-8 -*-
"""
Created on Tue Jul 18 11:02:20 2023

@author: ValentinLeLay
"""

import viager.report

inputs = {
    "calculation_parameters": {
        "calculation_date": "2023-07-07",
        "calculation_mode": 1,
        "expected_loss_to_fail_scenario": 0,
        "annual_time_steps": 1,
        "projection_years": 60,
        "mortality_diversification": True,
        "global_scenarios": [0],
        "loss_quantile_to_use": -1,
        "discount_losses": False,
        "use_default_garanti_fee": False,
        "default_garanti_fee": 0.0,
        "verbose": True,
        "mortality_release_date": "2023-07-07",
        "immo_release_date": "2023-07-07"},
    "borrowers": [
        {"birth_date": "1950-01-01",
         "gender": 2,
         "income_quantile": 14,
         "revenu" : 0,
         "alive": True}
         ,
        {"birth_date": "1963-01-01",
         "gender": 2,
         "income_quantile": 14,
         "revenu" : 0,
         "alive": True}
         ],
    "collateral_asset": {
        "real_estate_type": 1,
        "last_price_estimation_date": "2022-07-04",
        "last_price_estimation": 350000,
        "loyer_estimation" : 1950,
        "surface" : 150,
        "insee_code": "69123"},
    "loan_terms": {
        "already_issued": True,
        "issue_date": "2022-07-04",
        "initial_outstanding": 1.0,
        "grace_period": 0.25,
        "quotity": None,
        "levier_taux_variable": 1,
        "default_asset_liability_rate_were_applied": True,
        "interest_rate_or_margin": 0.0395},
    "liability_financing": {
        "already_issued": True,
        "issue_date": "2022-07-04",
        "initial_outstanding": 1.0,
        "levier_taux_variable": 0,
        "interest_rate_or_margin": 0.034067,
        "default_asset_liability_rate_were_applied": True},
    "viager" : {
        "methode_calculation_DUH" : 1,
        "methode_calculation_rentes" : 1,
        "pourcentage_bouquet" : 0.3,
        "taux_reversion" : 1.0,
        "taux_indexation_rente" : 0.0161,
        "taux_interet_technique" : 0.035,
        "taux_credit_immo" : 0.035,
        "taux_actualisation_DUH" : 0.03,
        "revenu_net_imposable_foyer" : 20000,
        "quotient_familial" : 1,
        "charges_deductibles" : 1000,
        "taux_moyen_imposition" : 0.11,
        "taxe_fonciere" : 1000,
        "charges_entretien" : 500,
        "taxe_ordures_menageres" : 300,
        "duree_contrat_a_terme" : 20
        }
}

result = viager.report.build_report(inputs)
