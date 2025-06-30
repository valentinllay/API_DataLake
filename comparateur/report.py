# -*- coding: utf-8 -*-
"""
Created on Tue Jul 18 11:59:15 2023

@author: ValentinLeLay
"""

import viager.report
import reversemortgage.report

def build_report(inputs):
    
    results = dict()
    
    #### Viager ####
    viager_results = viager.report.build_report(inputs)
    results["viager"] = viager_results

    #### Reversemortgage ####
    reversemortgage_results = reversemortgage.report.build_report(inputs)
    results["reversemortgage"] = reversemortgage_results
    # Varibles fixe pour les frais
    results["reversemortgage"]["Base Case"]["logs"]["loan_log"]["estimation_frais_client"] = 0.0825
    
    return results



def test_report_all():
    print("report_all")
