# -*- coding: utf-8 -*-
"""
Created on Fri Jul 11 11:01:52 2025

@author: ValentinLeLay

security.py
"""

from functools import wraps
from flask import request, g
from config import config
import logging

from errors.exceptions import AuthenticationError

logger = logging.getLogger(__name__)

def require_api_key(fn):
    """
    Décorateur Flask pour protéger un endpoint par clé API.

    - Vérifie que le header X-API-KEY correspond à une entrée de config.VALID_API_KEYS.
    - En cas d’échec, lève AuthenticationError.
    - Stocke g.user, logge l’appel, puis exécute la fonction décorée.
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        key = request.headers.get("X-API-KEY")
        user = config.VALID_API_KEYS.get(key)
        if not user:
            raise AuthenticationError("Invalid or missing API Key")
        g.user = user
        logger.info(f"Appel effectué par {g.user}")
        return fn(*args, **kwargs)
    return wrapper



