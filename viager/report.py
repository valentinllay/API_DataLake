# -*- coding: utf-8 -*-
"""
Created on Tue Jul 18 10:32:07 2023

@author: ValentinLeLay
"""

import viager.calculs
import viager.mortality
import viager.financial


def build_report(inputs: dict) -> dict:
    ######## INPUTS ########
    # inputs obligatoires
    date_naissance_1 = str(inputs["borrowers"][0]["birth_date"])
    gender_1 = int(inputs["borrowers"][0]["gender"])
    valeur_venale = float(inputs["collateral_asset"]["last_price_estimation"])
    # inputs optionnels
    date_naissance_2, gender_2 = None, None
    if len(inputs["borrowers"]) >=2:
        date_naissance_2 =  inputs["borrowers"][1]["birth_date"]
        gender_2 = inputs["borrowers"][1]["gender"]
    taux_indexation_rente = 0.02
    pourcentage_bouquet = 20
    
    ######## esperance_vie ########
    age_1 = viager.mortality.get_age(date_naissance_1)
    age_2 = viager.mortality.get_age(date_naissance_2)
    age_H, age_F = get_age_H_age_F(age_1,age_2,gender_1,gender_2)

    # Homme ou femme seul
    if age_2 is None:
        if gender_1 == 1:
            esperance_vie = viager.calculs.calcul_esperance_vie_homme_seul(age_H = age_1)
        elif gender_1 == 2:
            esperance_vie = viager.calculs.calcul_esperance_vie_femme_seul(age_F = age_1)
    # Couple Hétérosexuel avec faible difference d'age
    elif gender_1 != gender_2 and verif_difference_age_calculs(age_H, age_F):
        esperance_vie = viager.calculs.calcul_esperance_vie_couple_hetero_diff_age_faible(age_H, age_F)
    # Couple avec difference d'âge très élevée : tg05 puis recalibration
    # elif not verif_difference_age_calculs(age_H, age_F) or gender_1 == gender_2:
    else:
        df_tg05_1 = viager.mortality.get_tg05(gender_1, date_naissance_1)
        # print(f"{df_tg05_1=}")
        df_tg05_2 = viager.mortality.get_tg05(gender_2, date_naissance_2)
        # print(f"{df_tg05_2=}")
        df_mortalite = viager.mortality.get_tg05_couple(df_tg05_1, df_tg05_2)
        # print(f"{df_mortalite=}")
        esperance_vie_tg05 = viager.mortality.esperance_vie(df_mortalite)
        esperance_vie = viager.calculs.calibration_esperance_vie(esperance_vie_tg05)
   
    ###### DUH, usufruit, taux_rente ######
    taux_rente = round(viager.calculs.estimation_taux_rente(esperance_vie),2)
    DUH = round(viager.calculs.estimation_DUH(esperance_vie),2)
    usufruit = round(viager.calculs.estimation_usufruit(esperance_vie),2)
    
    ##### Impôts #####
    taux_moyen_imposition = 0.11
    taux_prelevements_sociaux = 0.172
    # abattement_fiscal =  0.5 # A FAIRE
    age_plus_eleve = viager.mortality.age_plus_eleve(date_naissance_1, date_naissance_2)
    abattement_fiscal = viager.financial.abattement_fiscal(age_plus_eleve)
    
    ###### Results ######
    results = compute_and_generate_results(esperance_vie, usufruit, DUH,
                   taux_rente, pourcentage_bouquet, valeur_venale)
    
    results_log = generate_log_results(date_naissance_1, date_naissance_2,
                   gender_1, gender_2, age_1, age_2, age_H, age_F,
                   esperance_vie, taux_rente, DUH, usufruit, pourcentage_bouquet,
                   valeur_venale, taux_indexation_rente, taux_moyen_imposition,
                   taux_prelevements_sociaux, abattement_fiscal)
    
    results.update(results_log)

    return results
        
        
    

def verif_difference_age_calculs(age_H, age_F):
    if age_H is None or age_F is None:
        return False
    cpt_verif = 0
    if age_H >= age_H and age_H-age_F<=20:
        cpt_verif += 1
    if age_F >= age_H and age_F-age_H<=10:
        cpt_verif += 1
    if cpt_verif ==2:
        return True



def get_age_H_age_F(age_1,age_2,gender_1,gender_2):
    age_H, age_F = None, None
    if gender_1 == gender_2:
        return age_H, age_F
    # age_1
    if gender_1 == 1:
        age_H = age_1
    elif gender_1 == 2:
        age_F = age_1
    # age_2
    if gender_2 is not None:
        if gender_2 == 1:
            age_H = age_2
        elif gender_2 == 2:
            age_F = age_2
    return age_H, age_F


def verif_inputs_utilisateur(date_naissance_1, date_naissance_2, gender_1,
                             gender_2, pourcentage_bouquet, valeur_venale):
    pass


def compute_and_generate_results(esperance_vie, usufruit, DUH, taux_rente,
                                 pourcentage_bouquet, valeur_venale):
    pourcentage_bouquet = pourcentage_bouquet/100
    taux_rente = taux_rente/100
    DUH = DUH/100
    usufruit = usufruit/100
    results = dict()
    results["viager_occupe_avec_rente"] = dict()
    results["viager_occupe_avec_rente"]["bouquet"] = round(((1-DUH)*valeur_venale)*pourcentage_bouquet)
    results["viager_occupe_avec_rente"]["rente"] =  round(((1-DUH)*valeur_venale)*(1-pourcentage_bouquet)*taux_rente)
    results["viager_occupe_sans_rente"] = dict()
    results["viager_occupe_sans_rente"]["bouquet"] = round((1-DUH)*valeur_venale)
    results["viager_occupe_sans_rente"]["rente"] =  0
    results["nue_pro"] = dict()
    results["nue_pro"]["bouquet"] = round(((1-usufruit)*valeur_venale))
    results["nue_pro"]["rente"] = 0
    return results

def generate_log_results(date_naissance_1, date_naissance_2, gender_1,
                         gender_2, age_1, age_2, age_H, age_F, esperance_vie,
                         taux_rente, DUH, usufruit, pourcentage_bouquet,
                         valeur_venale,taux_indexation_rente, taux_moyen_imposition,
                         taux_prelevements_sociaux, abattement_fiscal):
    results = dict()
    results["log"] = dict()
    results["log"]["date_naissance_1"] = date_naissance_1
    results["log"]["date_naissance_2"] = date_naissance_2
    results["log"]["gender_1"] = gender_1
    results["log"]["gender_2"] = gender_2
    results["log"]["age_1"] = age_1
    results["log"]["age_2"] = age_2
    results["log"]["age_H"] = age_H
    results["log"]["age_F"] = age_F
    results["log"]["esperance_vie"] = esperance_vie
    results["log"]["taux_rente"] = taux_rente
    results["log"]["DUH"] = DUH
    results["log"]["usufruit"] = usufruit
    results["log"]["pourcentage_bouquet"] = pourcentage_bouquet
    results["log"]["valeur_venale"] = valeur_venale
    results["log"]["taux_indexation_rente"] = taux_indexation_rente
    results["log"]["taux_moyen_imposition"] = taux_moyen_imposition
    results["log"]["taux_prelevements_sociaux"] = taux_prelevements_sociaux
    results["log"]["abattement_fiscal"] = abattement_fiscal
    return results

