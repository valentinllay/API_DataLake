# -*- coding: utf-8 -*-
"""
Created on Tue Jul 18 10:32:17 2023

@author: ValentinLeLay
"""

import pandas as pd


######### DUH ############
def DUH_viager(df_tg05, taux_actualisation_DUH, loyer_annuel):
    return usufruit_viager(df_tg05, taux_actualisation_DUH, loyer_annuel, taxe_fonciere = 0)

def DUH_a_terme(duree_demembrement,  taux_actualisation_DUH, loyer_annuel):
    return usufruit_a_terme(duree_demembrement, taux_actualisation_DUH, loyer_annuel, taxe_fonciere = 0)

########## USUFRUIT ###########
def usufruit_viager(df_tg05, taux_actualisation_DUH, loyer_annuel, taxe_fonciere):
    df_actualisation = pd.Series([(1+taux_actualisation_DUH)**(-t) for t in range(0,len(df_tg05))])
    usufruit_viager = (loyer_annuel+taxe_fonciere) * sum(df_actualisation * df_tg05["l(x+k)/l(x)"])
    return usufruit_viager

def usufruit_a_terme(duree_demembrement,  taux_actualisation_DUH, loyer_annuel, taxe_fonciere):
    df_actualisation = pd.Series([(1+taux_actualisation_DUH)**(-t) for t in range(0,duree_demembrement)])
    usufruit_a_terme = (loyer_annuel+taxe_fonciere) * sum(df_actualisation)
    return usufruit_a_terme

# TODO a mettre dans estimation
########### Avec données Yanport  #####################
def get_loyer_annuel(surface, prix_m2):
    # rendement_locatif = get_rendement_locatif(insee_code)
    # valeur_bien = prix_m2 * surface
    # loyer_annuel = rendement_locatif*valeur_bien
    pass
    
def get_loyer_annuel_2(surface):
    print("attention développement en cours, on utilise un loyer moyen au m2 de 13€ pour l'instant")
    loyer_moyen_m2 = 13
    loyer_mensuel = loyer_moyen_m2 * surface
    loyer_annuel = loyer_mensuel * 12
    return loyer_annuel
    
def get_rendement_locatif(insee_code):
    # TODO extraire rendement locatifs 2023 par zicode (puis faire pondération avec pop pour l'avoir par strate)
    # renvoie par strate 
    pass


############# RENTE ###############
def coeff_diviseur_viager(df_tg05, taux_interet_technique, taux_reversion):
    df_actualisation = pd.Series([(1+taux_interet_technique)**(-k) for k in df_tg05.index])
    if taux_reversion is not None:
        df_tg05_couple = df_tg05
        coeff_diviseur = sum(df_tg05_couple["deux_en_vie"][1:]*df_actualisation[1:])\
        + taux_reversion*sum(df_tg05_couple["un_seul_en_vie"][1:]*df_actualisation[1:])
        return coeff_diviseur
    coeff_diviseur = sum(df_tg05["l(x+k)/l(x)"][1:] * df_actualisation[1:])
    return coeff_diviseur

def coeff_diviseur_a_terme(duree_demembrement, taux_interet_technique):
    df_actualisation = pd.Series([(1+taux_interet_technique)**(-t) for t in range(0,duree_demembrement)])
    coeff_diviseur = sum(df_actualisation)
    return coeff_diviseur

def coeff_diviseur_viager_libre(esperance_vie, taux_credit_immo):
    capital_a_rembourser = 100
    reste_a_rembourser = [capital_a_rembourser - k*(capital_a_rembourser/esperance_vie) for k in range(round(esperance_vie))]
    interets = [taux_credit_immo*reste for reste in reste_a_rembourser]
    somme_interets = sum(interets)
    annuites = (capital_a_rembourser+somme_interets)/esperance_vie
    coeff_diviseur_viager_libre = capital_a_rembourser/annuites
    return coeff_diviseur_viager_libre

############# IMPOTS ###############
def abattement_fiscal(age_plus_eleve):
    age = age_plus_eleve
    if age < 50:
        abattement = 0.3
    elif age >= 50 and age <= 59:
        abattement = 0.5
    elif age > 59 and age <= 69:
        abattement = 0.6
    else:
        abattement = 0.7
    return abattement

def rente_imposable(rente_annuelle, abattement):
    return rente_annuelle - rente_annuelle*abattement

def revenu_imposable_total(rente_imposable, autre_revenu, charges_deductibles):
    return rente_imposable + autre_revenu - charges_deductibles

def impot_revenu(revenu_imposable_total, taux_moyen_imposition):
    return revenu_imposable_total * taux_moyen_imposition

def prelevements_sociaux(revenu_imposable_total, taux_prelevements_sociaux):
    return revenu_imposable_total * taux_prelevements_sociaux

def impot_total(impot_revenu, prelevements_sociaux):
    return impot_revenu + prelevements_sociaux







def test_financial():
    print("financial")
    
    
    # OLD
# def impots_revenu_et_tranches(revenu, quotient_familial):
#     revenu = float(revenu)
#     revenu = revenu/quotient_familial
#     liste_assiettes_max =  [10777.0, 16701.0, 51092.0, 90424.0, np.inf]
#     impots_par_assiette = [0, 0.11, 0.3, 0.41, 0.45]
#     assiettes = []
#     reste = revenu
#     for assiette_max in liste_assiettes_max:
#         if reste <= assiette_max:
#             assiettes.append(reste)
#             reste = 0
#         else:
#             assiettes.append(assiette_max)
#             reste -= assiette_max
#     impot_revenu = np.dot(assiettes, impots_par_assiette)
#     impot_revenu = impot_revenu * quotient_familial
#     tranche_imposition = get_tranche_imposition(assiettes, impots_par_assiette)
#     return impot_revenu, tranche_imposition

# def coeff_diviseur(age, df_tg05, taux_interet_technique):
#     """
#     https://www.spac-actuaires.fr/lexique/table-de-mortalite/
#     x   : age
#     lx  : nb de survuvants à l'âge x dans la table de mortalité
#     kpx : proba de survivre k ans à l'age x
#     vk  : vecteur des taux d'actualisations futurs
#     """
#     lx = df_tg05[age]
#     kpx = [df_tg05[age+k]/lx for k in range(1,len(df_tg05[age:]))] # Proba de survie 1 an de plus, 2 ans de plus, etc...
#     vk = [(1+taux_interet_technique)**(-k) for k in range(1,len(df_tg05[age:]))]
#     ax = np.dot(kpx, vk)
#     coeff_diviseur = ax
#     return coeff_diviseur

#     usufruit = valeur_venale - valeur_venale / ((1+taux_rendement_locatif)**esperance_vie)
# def calcul_DUH_methode_2(loyer_annuel, coeff_diviseur):
#     DUH = loyer_annuel * coeff_diviseur
#     return DUH

# def calcul_rentes_methode_1(capital_a_renter, coeff_diviseur, esperance_vie):
#     rentes = [capital_a_renter / coeff_diviseur]*round(esperance_vie)
#     return rentes

# def calcul_rentes_methode_2(capital_a_renter, esperance_vie, taux_interet_technique):
#     rentes = [(capital_a_renter / esperance_vie) * (1 + taux_interet_technique) ** t for t in range(1, esperance_vie+1)]
#     return liste

# def calcul_DUH(methode_calculation_DUH, loyer_annuel, coeff_diviseur, esperance_vie, taux_actualisation_DUH):
#     if methode_calculation_DUH == 1:
#         return calcul_DUH_methode_1(esperance_vie, loyer_annuel, taux_actualisation_DUH)
#     elif methode_calculation_DUH == 2:
#         return calcul_DUH_methode_2(loyer_annuel, coeff_diviseur)

# def usufruit(valeur_venale, loyer_annuel, esperance_vie):
#     taux_rendement_locatif = loyer_annuel / valeur_venale
#     return usufruit

# def calcul_rentes(methode_calculation_rentes, capital_a_renter, coeff_diviseur, esperance_vie, taux_interet_technique):
#     if methode_calculation_rentes == 1:
#         return calcul_rentes_methode_1(capital_a_renter, coeff_diviseur, esperance_vie)
#     elif methode_calculation_rentes == 2:
#         return calcul_rentes_methode_2(capital_a_renter, esperance_vie, taux_interet_technique)

# def revalorisation_rente(rentes, taux_revalorisation_rente):
#     rentes_revalorisees_brut = []
#     t = 0 # convention : on commence à 0 car on ne recoit pas une rente qui a deja capitalisée alors que l'année ne s'est à peine écoulée
#     for rente in rentes:
#         rentes_revalorisees_brut.append(rente*(1+taux_revalorisation_rente)**t)
#         t += 1
#     return rentes_revalorisees_brut

# def impots_revenu_et_tranches(revenu, quotient_familial):
#     revenu = float(revenu)
#     revenu = revenu/quotient_familial
#     liste_assiettes_max =  [10777.0, 16701.0, 51092.0, 90424.0, np.inf]
#     impots_par_assiette = [0, 0.11, 0.3, 0.41, 0.45]
#     assiettes = []
#     reste = revenu
#     for i,assiette_max in enumerate(liste_assiettes_max):
#         if reste <= assiette_max:
#             assiettes.append(reste)
#             reste = 0
#         else:
#             assiettes.append(assiette_max)
#             reste -= assiette_max
#     impot_revenu = np.dot(assiettes, impots_par_assiette)
#     impot_revenu = impot_revenu * quotient_familial
#     tranche_imposition = get_tranche_imposition(assiettes, impots_par_assiette)
#     return impot_revenu, tranche_imposition

# def get_tranche_imposition(assiettes, impots_par_assiette):
#     tranche_imposition = 0.45
#     for i,assiette in enumerate(assiettes):
#         if assiette == 0:
#             tranche_imposition = impots_par_assiette[i-1]
#             break
#     return tranche_imposition

# def impot_revenu_et_tranches_liste(liste_rentes_brutes_revalorisees, abattement_fiscal, quotient_familial):
#     rentes_imposable = [rente*abattement_fiscal for rente in liste_rentes_brutes_revalorisees]
#     nested_list = [impots_revenu_et_tranches(rente, quotient_familial) for rente in rentes_imposable]
#     liste_impots_revenu, liste_tranches_imposition = map(list, zip(*nested_list, strict=True))
#     return liste_impots_revenu, liste_tranches_imposition