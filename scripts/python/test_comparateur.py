# -*- coding: utf-8 -*-
"""
Created on Tue Jul 18 11:03:45 2023

@author: ValentinLeLay
"""

import comparateur.report


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

results = comparateur.report.build_report(inputs)
print(results)

 





# ANCIENS TESTS

# Verifier inputs
# if "last_price_estimation" not in inputs["collateral_asset"]\
#     or "loyer_estimation" not in inputs["collateral_asset"]\
#     and "surface" not in inputs["collateral_asset"]:
#         print("ERREUR : On doit renseigner la surface si on ne renseigne pas valeur_venale ET loyer_mensuel")
# if not isinstance(inputs["viager"]["duree_contrat_a_terme"],int) : # mieux que type() : instance
#     print("erreur, veuillez entrer un int pour duree_contrat_a_terme")
# def verif_parameters(age_1, age_2, age_H, age_F, gender_1, gender_2):
#     elif (age_H is not None) and (age_H < 40 or age_H > 105):
#         return False
#     elif (age_F is not None) and (age_F < 40 or age_F > 105):
#         return False
#     return True

# Creation tableau données pour toutes les combinaisons d'age H et F (age entre 40 et 105 ans)
# from tqdm import tqdm
# import time
# df = pd.read_csv("TABLE_DAUBRY_COUPLE.csv", sep = ";")
# arr_age_H_F = df[["AGE_H","AGE_F"]].values

# final_df = pd.DataFrame()
# for i in tqdm(range(len(arr_age_H_F))):
#     tupple = arr_age_H_F[i]
#     age_H = tupple[0]
#     age_F = tupple[1]
#     birth_year_H = 2023 - age_H
#     birth_year_F = 2023 - age_F
#     inputs["borrowers"][0]["birth_date"] = str(birth_year_H) + '-01-01'
#     inputs["borrowers"][1]["birth_date"] = str(birth_year_F) + '-01-01'
#     # print(inputs["borrowers"][0]["birth_date"])
#     # print(inputs["borrowers"][1]["birth_date"])
#     print()
#     results = comparateur.report_all.all_in_report(inputs)
#     print(results["viager"]["log"])
#     dic = results["viager"]["log"]
#     temp_df = pd.json_normalize(dic)
#     final_df = pd.concat([final_df,temp_df])
# Sauvegarde 
# final_df_sortedbyECdaubry = final_df.sort_values("daubry.ESPERANCE_VIE_COUPLE", ascending = False)
# final_df_sortedbyECdaubry.to_csv("calculs_vs_daubry_couples_sortedbyECdaubry3.csv", sep = ";", index = False)
# final_df_sortedbyECdaubry.to_excel("calculs_vs_daubry_couples_sortedbyECdaubry3.xlsx")
# Sauvegarde 
# final_df.to_csv("Homme_Homme.csv", sep = ";", index = False)
# final_df_sortedbyECval.to_excel("calculs_vs_daubry_couples_sortedbyECval3.xlsx")



######### Homme Seul ############
# liste_df = []
# inputs["borrowers"][1]["birth_date"] = None
# for age_H in range(40, 105+1):
#     birth_year_H = 2023 - age_H
#     inputs["borrowers"][0]["birth_date"] = str(birth_year_H) + '-01-01'
#     results = comparateur.report_all.all_in_report(inputs)
#     results["viager"]["log"]
#     dic = results["viager"]["log"]
#     temp_df = pd.json_normalize(dic)
#     liste_df.append(temp_df)
# final_df = pd.concat(liste_df)
# # final_df.to_csv("calculs_vs_daubry_H.csv", sep = ";", index = False)
# final_df










