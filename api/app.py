# -*- coding: utf-8 -*-
"""
Created on Fri Jul 11 11:01:52 2025

@author: ValentinLeLay

app.py
"""

import logging
from flask import Flask, jsonify, request, g, Response

from config import config
from validators import validate_maximum_quotity_payload, validate_greeting_payload
from services import get_maximum_quotity, get_generic_greeting, get_personalized_greeting
from security import require_api_key
from errors.exceptions import InputValidationError, AuthenticationError, NotFoundError, DatabaseError
import reversemortgage.report_simplified


logging.basicConfig(level=config.LOG_LEVEL)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['DEBUG'] = config.DEBUG
app.config['TESTING'] = config.TESTING

### ENDPOINTS ###
# TODO : faire une /v2 avec un champs "field" pour récupérer autre chose que max quo de façon paramétrique.
@app.route("/v1/maximum_quotity", methods=["POST"])
def calculs_ltv_maximum_quotity():
    """
    Expose la quotité maximale selon les filtres donnés.
    """
    data = request.get_json() or {}
    payload = validate_maximum_quotity_payload(data)
    mq = get_maximum_quotity(**payload)
    return jsonify({"result": mq}), 200


@app.route("/hello_world", methods=["GET"])
def hello_world():
    """
    Endpoint GET pour salutation générique.
    """
    result: str = get_generic_greeting()
    return jsonify({"result": result}), 200


@app.route("/hello_world_secured", methods=["GET"])
@require_api_key
def hello_world_secured():
    """
    Endpoint pour salutation générique sécursié par clé API.
    """
    result: str = get_generic_greeting()
    return jsonify({"result": result}), 200


@app.route("/bonjour", methods=["POST"])
def bonjour():
    """
    Endpoint pour salutation personnalisée via POST.
    Récupère les paramètres dans le corps JSON.
    """
    data: dict = request.get_json() or {}
    validated = validate_greeting_payload(data)
    result: str = get_personalized_greeting(**validated)
    return jsonify({"result": result}), 200


# TODO : ajouter "/v1"
@app.route("/calculation_simplified", methods=["POST"])
def calculation_simplified() -> tuple[Response, int]:
    """
    Endpoint bidon pour calcualtion LTV.
    Les paramètres sont dans le corps JSON.
    """
    data = request.get_json()
    raise_if_force_error(data)
    results: dict = reversemortgage.report_simplified.build_report(data)
    return jsonify({"result": results}), 200


@app.route('/comparateur_viager', methods=['POST'])
#@jwt_required()
def comparateur_viager():

    # result = comparateur.report.build_report(request.get_json())
    result = "[ERR] pas implémenté."
    return jsonify({"result": result}), 200


### HANDLERS D'ERREUR ###
# Les handlers d’exception “métier”
@app.errorhandler(InputValidationError)
def handle_bad_input(e):
    return jsonify({'status':'error','error': str(e)}), 400

@app.errorhandler(AuthenticationError)
def handle_auth_error(e):
    return jsonify({'status': 'error', 'error': str(e)}), 401

@app.errorhandler(NotFoundError)
def handle_not_found(e):
    return jsonify({'status':'error','error': str(e)}), 404

@app.errorhandler(DatabaseError)
def handle_bad_database(e):
    return jsonify({'status':'error','error': str(e)}), 404

# Les handlers de codes HTTP bruts
@app.errorhandler(400)
def handle_400(e):
    return jsonify({'status': 'error', 'error': str(e)}), 400

@app.errorhandler(404)
def handle_404(e):
    return jsonify({'status': 'error', 'error': str(e)}), 404

@app.errorhandler(405)
def handle_405(e):
    return jsonify({'status':'error','error':'Method Not Allowed'}), 405

@app.errorhandler(500)
def handle_500(e):
    return jsonify({'status': 'error', 'error': 'Internal server error'}), 500


### UTILS ###
@app.after_request
def clear_user(response):
    """
    Réinitialise g.user après chaque requête
    pour éviter toute fuite de contexte entre appels.
    """
    g.user = None
    return response

def raise_if_force_error(data: dict) -> None:
    """
    Vérifie le champ `force_error` dans le JSON et, si activé,
    lève une RuntimeError pour déclencher le debugger interactif de Flask.

    Args:
        data (dict): Données extraites de `request.get_json()`.

    Raises:
        RuntimeError: si `force_error` (insensible à la casse) vaut
        "1", "yes" ou "true".
    """
    # Si on passe ?force_error=1, on lève volontairement
    force_error = str(data.get("force_error", "")).lower()
    if force_error in ("1", "yes", "true"):
        raise RuntimeError("Test volontaire du debugger")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=config.DEBUG)

