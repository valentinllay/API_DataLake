# api/rate_limit.py
"""
Module api/rate_limit.py
Configuration de Flask-Limiter (stockage en mémoire) avec clé combinant IP et user_email,
et enregistrement du hook de logging.
"""
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask import request


def _rate_limit_key() -> str:
    """
    Génère une clé de rate-limit unique par IP et user_email.
    Si user_email est absent, on se rabat uniquement sur l'IP.

    Returns:
        str: clé de limitation.
    """
    # Récupération de l'IP du client
    ip = get_remote_address() or ""
    # Tentative de récupération de l'email depuis le payload JSON
    try:
        payload = request.get_json(silent=True) or {}
        email = payload.get("user_email") or ""
    except Exception:
        email = ""
    # Clé combinée
    return f"{ip}:{email}"

# Initialisation du Limiter global en mémoire
limiter = Limiter(
    key_func=_rate_limit_key,
    default_limits=["720 per minute"],
    storage_uri="memory://"
)

def init_rate_limit(app) -> None:
    """
    Initialise Flask-Limiter sur l'application et enregistre
    le hook de logging avant chaque requête.

    Args:
        app: instance Flask
    Returns:
        None
    """
    limiter.init_app(app)
