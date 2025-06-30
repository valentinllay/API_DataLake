# -*- coding: utf-8 -*-
"""
Created on Tue Jul 18 10:29:39 2023

@author: ValentinLeLay
"""

import numpy as np


###### Modélisation esperance de vie pour couples hétéro et difference faible d'age ######

def calcul_esperance_vie_couple_hetero_diff_age_faible(age_H, age_F):
    """"
    Voir script modélisation epserance_vie avec age_1 et age_2.py dans folder calibration et tests pour voir toutes les autres fonctions "poly" de modélisation.
    """
    def func_poly_4_bis(xy, a, b, c, d, e, f, g, h, i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x_,y_):
        x, y = xy
        return a + b*x + c*y + d*x*y + e*x**2 + f*y**2 + g*x*y**2 + h*y*x**2 + i*x**2*y**2 + j*x**3 + k*y**3 + l*x*y**3 + m*x**2*y**3 + n*x**3*y**3 + o*y*x**3 + p*y**2*x**3  + q*y**4 + r*x*y**4 + s*x**2*y**4 + t*x**3*y**4 + u*x**4*y**4 + v*x**4 + w*y*x**4 + x_*y**2*x**4 + y_*y**3*x**4 
    popt = np.array([ 2.29835096e+01,  5.91268816e+01, -5.13643285e+01, -1.27222328e+00,-2.22564785e+00,  3.08741007e+00, -4.42388234e-02,  8.54237246e-02,-5.71986406e-04,  3.26243086e-02, -6.40618373e-02,  1.56565279e-03,-1.09101665e-05, -5.27213830e-08, -1.45141925e-03,  1.89996501e-05, 4.89604627e-04, -1.48579812e-05,  1.68508756e-07, -6.89269924e-10, -1.03802080e-13, -1.63688541e-04,  7.88622495e-06, -1.22850500e-07, 7.25972862e-10])
    X_H, X_F = age_H, age_F
    Y_ = func_poly_4_bis((X_H,X_F), *popt)
    esperance_vie_ = Y_
    return esperance_vie_

def calcul_esperance_vie_homme_seul(age_H):
    def func3(X,a,b,c,d,e):
        return  e*X**4 + d*X**3 + c*X**2 + b*X + a
    popt = np.array([ 4.50351063e+01,  1.26295727e+00, -5.13898429e-02,  5.01244153e-04,-1.55203503e-06])
    X = age_H
    esperance_vie_ = func3(X, *popt)
    return esperance_vie_

def calcul_esperance_vie_femme_seul(age_F):
    def func3(X,a,b,c,d,e):
        return  e*X**4 + d*X**3 + c*X**2 + b*X + a
    popt = np.array([ 6.81741651e+01,  2.65404312e-02, -1.85007703e-02,  1.22453334e-04, -4.61695098e-08])
    X = age_F
    esperance_vie_ = func3(X, *popt)
    return esperance_vie_


###### CALCULS ######
def calibration_esperance_vie(esperance_vie_tg05): # estimation_esperance_vie_daubry
    """
    utile pour les couples Homme_Homme et Femme_Femme.
    recalibre une esperance de vie calculée avec TG05.
    on utilise la fonction psi_couple pour cette transformaation.
    """
    def psi_couple(x):
        a,b,c,d,e = [2.04258525e+00, 6.13148675e-01,  1.43202883e-02, -3.32657913e-04, 2.81642517e-06]
        return a + b*x + c*x**2 + d*x**3 + e*x**4
    esperance_vie_apres_calibration = psi_couple(esperance_vie_tg05)
    return esperance_vie_apres_calibration

def estimation_taux_rente(esperance_vie):
    """
    Cette fonction permet d'approximer la courbe esperance de vie vs taux de rente qui a une forme en 1/X. 
    Je modélise ensuite les erreurs de cette première approximation en 1/X
    Je modélise à nouveau les erreurs de la modélisation des erreurs précédents
    L'idée est donc de produire un modèle général dont on a modélisé successivement les erreurs des erreurs des erreurs...
    Le modèle initial est : Y_ et avec err1 = Y_ - Y
    après une première modélisation des erreurs : Y_ - err1_ et avec err2 = err1_ - err1
    après une deuxième modélisation des erreurs : Y_ - (err1_ - err2_) avec err3 = err2_ - err2
    si on modélise successivement les erreurs marginales on obtient le modèle : Y_ - (err1_ - (err2_ - (err3_ - (err4_ - ... - (errn_) )...))))
    """
    def func1(X, a, b, c):
        return a/X**b + c 
    def func3(X, a, b,c):
        return a/np.exp(b*X) + c
    def func5(X,a,b,c,d):
        return  d*X**3 + c*X**2 + b*X + a
    popt1 = [90.08934863, 1.00581785, 1.47686825]
    Y_ = func1(esperance_vie, popt1[0], popt1[1], popt1[2])
    popt2 = [2.17160980e+02, 3.05545514e+00, -8.49332679e-05]
    err1_ = func3(esperance_vie, popt2[0], popt2[1], popt2[2])
    popt3 = [8.72572718e-03, -1.64181366e-03,  7.51849623e-05, -9.47303486e-07]
    err2_ = func5(esperance_vie, popt3[0], popt3[1], popt3[2], popt3[3])
    taux_rente = Y_-(err1_-err2_)
    return taux_rente
    
def estimation_DUH(esperance_vie):
    """
    Idem mais pas besoin de modélisation des erreurs car c'était du bruit blanc
    """
    def func(X,a,b,c,d,e):
        return  e*X**4 + d*X**3 + c*X**2 + b*X + a
    popt = [1.01052709e+01,  3.11193863e+00, -5.15872038e-02,  4.85644825e-04, -2.09958616e-06]
    Y_ = func(esperance_vie, *popt)
    DUH = Y_
    return DUH

def estimation_usufruit(esperance_vie):
    """
    Idem mais pas besoin de modélisation des erreurs car c'était du bruit blanc
    """
    def func(X,a,b,c,d,e):
        return  e*X**4 + d*X**3 + c*X**2 + b*X + a
    popt = [6.20067747e-02, 3.46831725e+00, -5.79556237e-02, 5.54700314e-04, -2.45662109e-06]
    Y_ = func(esperance_vie, *popt)
    usufruit = Y_
    return usufruit


        
