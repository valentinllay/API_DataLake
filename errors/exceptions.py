# -*- coding: utf-8 -*-
"""
Created on Fri Jul 11 11:01:52 2025

@author: ValentinLeLay

exceptions.py
"""

class InputValidationError(Exception):
    """Paramètres invalides dans la requête JSON."""
    pass

class NotFoundError(Exception):
    """Aucun enregistrement trouvé pour les critères fournis."""
    pass

class DatabaseError(Exception):
    """Erreur inattendue au niveau de la base de données."""
    pass

class AuthenticationError(Exception):
    """Clé API manquante ou invalide."""
    pass