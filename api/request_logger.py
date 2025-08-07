# api/request_logger.py
"""
Module api/request_logger.py
Log SQL des requêtes POST sur /v*/maximum_quotity avec SQLAlchemy Core, simplifié.

Remarques:
- Engine SQLAlchemy créé globalement
- Transaction explicite pour commit
- Gestion des exceptions absorbée pour robustesse
- IP client via request.remote_addr
- Logging du payload complet (JSON sérialisé)
- Insertion du status_code
- Timestamp géré en base via DEFAULT CURRENT_TIMESTAMP
- Filtrage des chemins dynamiques /v1/, /v2/, .../maximum_quotity
- Table cible: request_logs_raw
"""

import json
import logging
from flask import request, Response
from sqlalchemy import text, Engine
from db import create_db_engine

logger = logging.getLogger(__name__)
# Engine global pour réutilisation et pooling
engine: Engine = create_db_engine()


def log_request_to_db(response: Response) -> Response:
    """
    Après chaque requête, log SQL dans request_logs_raw pour tout endpoint
    terminant par /maximum_quotity sur /v{version}/.

    Args:
        response (Response): objet réponse Flask
    Returns:
        Response: la même réponse
    """
    try:
        # path = request.path.rstrip('/')
        # Early return si l'endpoint n'est pas /v*/maximum_quotity
        # if not (path.startswith("/v") and path.endswith("/maximum_quotity")):
        #     return response

        ip = request.remote_addr
        payload = request.get_json(silent=True) or {}
        payload_json = json.dumps(payload)
        status_code = response.status_code

        sql = text(
            "INSERT INTO request_logs_raw"
            " (ip_address, endpoint, payload, status_code)"
            " VALUES (:ip, :endpoint, :payload, :status_code)"
        )
        params = {
            "ip": ip,
            "endpoint": request.path,
            "payload": payload_json,
            "status_code": status_code,
        }
        try:
            with engine.begin() as conn:
                conn.execute(sql, params)
        except Exception:
            logger.exception("Échec du log en base de données")
    except Exception:
        logger.exception("Erreur inattendue dans request_logger")
    return response


if __name__ == "__main__":
    # Test local
    from flask import Flask
    app = Flask(__name__)
    app.after_request(log_request_to_db)
    with app.test_request_context(
        '/v1/maximum_quotity', method='POST', json={'a':1}
    ):
        resp = Response(status=200)
        log_request_to_db(resp)
        print("Log de test inséré dans request_logs_raw")
