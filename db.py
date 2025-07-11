# -*- coding: utf-8 -*-
"""
Created on Fri Jul 11 11:01:52 2025

@author: ValentinLeLay

db.py
Module de gestion de la connexion à la base de données MySQL (AWS RDS) via SQLAlchemy Core.
Fournit une factory pour créer un engine singleton, configuré avec SSL et pool_pre_ping
pour garantir la robustesse et la sécurité des connexions.
"""

import os
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

from config import config

_engine = None

def create_db_engine(url: str | None = None) -> Engine:
    """
    Crée et retourne un SQLAlchemy Engine Core singleton.

    - Utilise l'URI et les options (pool_pre_ping, SSL CA, tailles de pool, overflow)
      centralisées dans config.py.
    - Ne reconstruit l'engine qu'une seule fois (singleton), pour éviter la surcharge
      de création de pools sur AWS RDS.
    - Garantit des connexions chiffrées via SSL et la validité des connexions existantes
      grâce au pre-ping.

    Args:
        url: Optionnel, URI de la base à utiliser (ex. SQLite in-memory pour les tests).
    Returns:
        Engine SQLAlchemy prêt à l’emploi.
    """
    global _engine
    # Choix de l'URI : override si fourni, sinon config
    database_uri = url or config.SQLALCHEMY_DATABASE_URI
    if _engine is None:
        _engine = create_engine(
            database_uri,
            pool_pre_ping=config.SQLALCHEMY_PRE_PING,
            connect_args={
                "ssl_ca": config.SSL_CA_PATH,
            }
        )
    return _engine




if __name__ == "__main__":
    # Test rapide de la connexion : affiche le Engine et tente une connexion ping
    print("SSL_CA_PATH =", config.SSL_CA_PATH)
    print("Fichier SSL existe ?", os.path.isfile(config.SSL_CA_PATH))
    engine = create_db_engine()
    print("Engine créé :", engine)
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("Connexion à la base réussie.")
    except Exception as e:
        print("Échec de la connexion :", e)