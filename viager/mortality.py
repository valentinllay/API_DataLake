# -*- coding: utf-8 -*-
"""
Created on Tue Jul 18 10:29:39 2023

@author: ValentinLeLay
"""
import numpy as np
import datetime
import pandas as pd
import os

from viager.scripts_utiles import get_data_path



####################### TABLE MORTALITE TG05 ###############################
def get_tg05(gender, date_naissance: str): # "%Y-%m-%d"
    """
    fonction get_tg05 :
    	- date de naissance mini en 2023 : 1906 (117 ans) -> donnera une proba de mort dans l'année de 1.
    	- date de naissance maxi : 2005
    	- si on entre une date de naissance après la date d'aujourd'hui on a 1 ligne de plus dans notre tg05
    """

    def ajouter_mortalite_marginale_tg05(df_tg05):
        l0 = df_tg05.loc[0,"cohorte"]
        kpx = [df_tg05.loc[k,"cohorte"]/l0 for k in range(len(df_tg05))]
        qxk = [1-df_tg05.loc[k+1,"cohorte"]/df_tg05.loc[k,"cohorte"] for k in range(len(df_tg05)-1)] + [1]
        mortalite_marginale = np.multiply(kpx,qxk)
        df_tg05["l(x+k)/l(x)"] = kpx
        df_tg05["1-l(x+k+1)/l(x+k)"] = qxk
        df_tg05["mortalite_marginale"] = mortalite_marginale
        # survie = [1-sum(mortalite_marginale[:k]) for k in range(len(mortalite_marginale))]
        # df_tg05["survie"] = survie
        return df_tg05

    def append_new_lines(df_tg05):
        final_size_df_tg05 = 120
        line = [0,0,1,0]
        nb_new_lines = final_size_df_tg05 - len(df_tg05)
        new_lines = np.array(line*nb_new_lines).reshape(nb_new_lines,len(line))
        new_lines = pd.DataFrame(new_lines, columns=['cohorte', 'l(x+k)/l(x)', '1-l(x+k+1)/l(x+k)', 'mortalite_marginale'])
        df_tg05 = pd.concat([df_tg05,new_lines], axis = "index")
        df_tg05.reset_index(inplace = True, drop = True)
        return df_tg05
    
    data_path = get_data_path()
    if gender == 1:
        file_path = os.path.join(data_path, "TGH05.csv")
        df_tg05 = pd.read_csv(file_path, sep = ";", index_col = 0)
    elif gender == 2:
        file_path = os.path.join(data_path, "TGF05.csv")
        df_tg05 = pd.read_csv(file_path, sep = ";", index_col = 0)
    age = get_age(date_naissance)
    birth_year = get_birth_year(date_naissance)
    df_tg05 = df_tg05.loc[age:, str(birth_year)]
    df_tg05 = df_tg05.reset_index(drop = True)
    df_tg05 = df_tg05.to_frame()
    df_tg05.columns = ["cohorte"]
    df_tg05 = df_tg05.loc[(df_tg05!=0).any(axis=1)]
    df_tg05 = ajouter_mortalite_marginale_tg05(df_tg05)
    df_tg05 = append_new_lines(df_tg05)
    return df_tg05

    
def get_tg05_couple(df_tg05_1, df_tg05_2):
    mortalite_marginale, kpx, deux_en_vie, un_seul_en_vie  = [], [], [], []
    for k in df_tg05_1.index:
        A = df_tg05_1["mortalite_marginale"][k] * df_tg05_2["mortalite_marginale"][k]
        B = sum(df_tg05_1["mortalite_marginale"][0:k]) * df_tg05_2["mortalite_marginale"][k]
        C = sum(df_tg05_2["mortalite_marginale"][0:k]) * df_tg05_1["mortalite_marginale"][k]
        mortalite_marginale.append(A + B + C)
        kpx.append(np.subtract(1,sum(mortalite_marginale[0:k])))
        deux_en_vie.append(df_tg05_1["l(x+k)/l(x)"][k] * df_tg05_2["l(x+k)/l(x)"][k])
        un_seul_en_vie.append(kpx[k] - deux_en_vie[k])
    df_tg05_couple = pd.DataFrame()
    df_tg05_couple["mortalite_marginale"] = mortalite_marginale
    df_tg05_couple["l(x+k)/l(x)"] = kpx
    df_tg05_couple["deux_en_vie"] = deux_en_vie
    df_tg05_couple["un_seul_en_vie"] = un_seul_en_vie
    return df_tg05_couple
    


def esperance_vie(df_tg05):
    K_half = [k+0.5 for k in df_tg05.index]
    esperance_vie = sum(df_tg05["mortalite_marginale"]*K_half)
    return esperance_vie

def age_plus_eleve(date_naissance_1, date_naissance_2):
    if date_naissance_2 is not None:
        return max(get_age(date_naissance_1), get_age(date_naissance_2))
    return get_age(date_naissance_1)

def get_age(date_naissance):
    if date_naissance is None:
        return None
    # NICETOHAVE NTH : adapter en fonction du format de la date.
    born = datetime.datetime.strptime(date_naissance,"%Y-%m-%d")
    today = datetime.date.today()
    age = today.year - born.year
    if today.month > born.month:
        return age
    elif today.month == born.month and today.day >= born.day:
        return age
    else:
        return age -1

def get_birth_year(date_naissance):
    birth = datetime.datetime.strptime(date_naissance,"%Y-%m-%d")
    birth_year = birth.year
    return birth_year

def test_mortality():
    print("mortality")
    
    
