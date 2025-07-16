# -*- coding: utf-8 -*-
"""
Created on Fri Jul 11 11:01:52 2025

@author: ValentinLeLay

config.py
Ce module centralise tous les paramètres et constantes de l’application,
notamment la configuration des connexions à la base de données pour les
environnements de production, développement et tests.
"""

import os
import logging

# Racine absolue du projet, pointe sur le dossier API_DataLake/
PROJECT_ROOT: str = os.path.dirname(os.path.abspath(__file__))

class Config:
    """
    Configuration de base (production par défaut).

    Attributs :
        DEBUG : activation ou non du mode debug Flask.
        LOG_LEVEL : niveau de verbosité des logs
        TESTING : activation du mode testing.
        DB_USER : nom d’utilisateur de la base.
        DB_PASSWORD : mot de passe de la base.
        DB_HOST : hôte RDS MySQL.
        DB_PORT : port MySQL (par défaut 3306).
        DB_NAME : nom de la base de données.
        SSL_CA_PATH : chemin vers le certificat RDS CA.
        SQLALCHEMY_DATABASE_URI : URI de connexion SQLAlchemy Core.
        VALID_API_KEYS : Clé d'API pour authentifier les connexions à certains endpoints.
    """
    DEBUG: bool = False
    LOG_LEVEL = logging.DEBUG if DEBUG else logging.INFO
    TESTING: bool = False

    # Informations de connexion (en clair)
    DB_USER: str = 'python_script'
    DB_PASSWORD: str = 'PCbN6ySghm6DaJFX6zN7oFXQosEfy4a99SHknSRY'
    DB_HOST: str = 'datalake-rds.cleg662om8fw.eu-west-3.rds.amazonaws.com'
    DB_PORT: int = 3306
    DB_NAME: str = 'reverse_mortgage_simulations'
    SSL_CA_PATH: str = os.path.join(PROJECT_ROOT, "resources", "SSL_CA_file", "eu-west-3-bundle.pem")

    # URI SQLAlchemy Core
    SQLALCHEMY_DATABASE_URI: str = (
        f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    )
    SQLALCHEMY_PRE_PING = True

    VALID_API_KEYS: dict[str] = {
        "Fb6yymHYdG7b7JhKJ9skHC4BMQTGgGiBmEfMo8A6": "CFCAL_user",
        "yhbBgzNycs5aY8rxdam3BAimGqMzi5XbMroNsbdL":  "ARRAGO_user"
    }


class DevelopmentConfig(Config):
    """
    Configuration pour l’environnement de développement.

    Par rapport à Config :
      - DEBUG activé
      - Identifiants et hôte pointant vers la DB de dev
    """
    DEBUG: bool = True


class TestingConfig(Config):
    """
    Configuration pour l’environnement de tests.

    Par rapport à Config :
      - TESTING activé
      - Identifiants et hôte pointant vers la DB de tests
    """
    TESTING: bool = True


class ProductionConfig(Config):
    """
    Configuration pour l’environnement de production.

    Hérite directement de Config sans modification.
    """
    pass

# Par défaut on utilise la configuration de production.
# Choix possible : ProductionConfig(), TestingConfig(), DevelopmentConfig()
config = ProductionConfig()


if __name__ == "__main__":
    # Test rapide de la configuration
    print("=== Vérification de la configuration ===")
    print(f"PROJECT_ROOT: {PROJECT_ROOT}")
    print(f"Config utilisée : {type(config).__name__}")
    print(f"DEBUG         : {config.DEBUG}")
    print(f"TESTING       : {config.TESTING}")
    print(f"DB_URI        : {config.SQLALCHEMY_DATABASE_URI}")
    print(f"SSL_CA_PATH   : {config.SSL_CA_PATH}")
    print("Fichier SSL existe ?", os.path.isfile(config.SSL_CA_PATH))
    print(f"Engine opts   : {config.SQLALCHEMY_ENGINE_OPTIONS}")
    print("========================================")
