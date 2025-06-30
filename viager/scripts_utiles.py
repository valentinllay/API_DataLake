# -*- coding: utf-8 -*-
"""
Created on Tue Jul 18 14:06:33 2023

@author: ValentinLeLay
"""

import pandas as pd
import numpy as np
import os


################## paths ##################
# def get_comparateur_path(): SUPPRIMER
#     comparateur_path = os.path.dirname(os.path.realpath('__file__'))
#     return comparateur_path

def get_log_path():
    log_path = os.path.join("viager","log")
    return log_path

def get_data_path():
    data_path = os.path.join("viager","data")
    return data_path


##################### DATA #########################

def get_insee_code_mapping():
    data_path = get_data_path()
    mapping_path = os.path.join(data_path,"Mapping.xlsx")
    mapping = pd.read_excel(
        mapping_path, 
        usecols = ["insee_code", "zip_code", "real_estate_type", "asset_category"],
        dtype={"real_estate_type": "int8", "asset_category": "int16"}) 
        # int8 can store integers from -128 to 127
        # int16 can store integers from -32768 to 32767
        # int64 can store integers from -9223372036854775808 to 9223372036854775807.
    return mapping

def get_prix_m2(insee_code, type_bien):
    data_path = get_data_path()
    if type_bien == 1:
        prix_m2_path = os.path.join(data_path,"prix_M2_annuel_par_zc_appart_Q50.csv")
    elif type_bien == 2:
        prix_m2_path = os.path.join(data_path,"prix_M2_annuel_par_zc_mais_Q50.csv")
    df_prix_m2 = pd.read_csv(prix_m2_path, sep = ";")
    df_prix_m2["date"] = pd.to_datetime(df_prix_m2['date'])
    zip_code, strate = get_zip_code_strate(insee_code, type_bien)
    prix_m2 = df_prix_m2[df_prix_m2["date"] == "2023-01-01"][f"Q50_{zip_code}"].values[0]    
    if np.isnan(prix_m2):
        prix_m2 = get_prix_m2_par_strate(strate)
    return prix_m2

def get_prix_m2_par_strate(strate):
    strate = int(strate)
    data_path = get_data_path()
    file_path = os.path.join(data_path, "PRIX_M2_Q50_pondere_par_strate_2019_YANPORT.csv")
    df_prix_m2 = pd.read_csv(file_path, sep = ";", dtype={"strate": "int16"}) 
    prix_m2 = df_prix_m2[df_prix_m2["strate"] == strate]["PRIX_M2_Q50"].values[0]
    return prix_m2
    
def get_strate(insee_code, type_bien):  
    insee_code = int(insee_code)
    mapping = get_insee_code_mapping()
    strate = mapping[(mapping["insee_code"] == insee_code) & (mapping["real_estate_type"] == type_bien)]["asset_category"].values[0]
    return strate

def get_zip_code_strate(insee_code, type_bien):
    insee_code = int(insee_code)
    type_bien = int(type_bien)
    mapping = get_insee_code_mapping()
    zip_code = mapping[mapping["insee_code"] == insee_code]["zip_code"].values[0]
    zip_code = add_zero(zip_code)
    strate = mapping[(mapping["insee_code"] == insee_code) & (mapping["real_estate_type"] == type_bien)]["asset_category"].values[0]
    return zip_code, strate
####################### END DATA #####################################



    
def add_zero(zip_code_or_insee_code):
    temp = zip_code_or_insee_code
    temp = str(temp)
    if len(temp) <= 4:
        return '0' + temp
    else:
        return temp

#

