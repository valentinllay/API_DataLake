from flask import Flask, jsonify, request

from hello_world.greet import say_hello_world, personalized_greeting
import reversemortgage.report
# import comparateur.report

app = Flask(__name__)

@app.route("/hello_world", methods=["GET"])
def hello():
    """
    Endpoint pour salutation générique.
    """
    message = say_hello_world()
    return jsonify({"message": message})


@app.route("/bonjour", methods=["POST"])
def bonjour():
    """
    Endpoint pour salutation personnalisée via POST.
    Récupère les paramètres dans le corps JSON.
    """
    data = request.get_json() or {}
    genre = data.get("genre")
    prenom = data.get("prenom")
    nom = data.get("nom")

    message = personalized_greeting(genre, prenom, nom)

    return jsonify({
        "message": message,
        "genre": genre,
        "prenom": prenom,
        "nom": nom
    })



@app.route("/calculation_simplified", methods=["POST"])
def calculation_simplified():
    """
    Endpoint bidon pour calcualtion LTV.
    Les paramètres sont dans le corps JSON.
    """
    data = request.get_json() or {}
    for field in ("real_estate_type", "insee_code"):
        if field not in data:
            return jsonify({"error": f"Le paramètre '{field}' est requis"}), 400

    results_simplified: dict = reversemortgage.report.build_report_simplified(inputs_simplified=data)

    return jsonify(results_simplified)



@app.route('/comparateur_viager', methods=['POST'])
#@jwt_required()
def comparateur_viager():

    # result = comparateur.report.build_report(request.get_json())
    result = "[ERR] pas implémenté."
    return jsonify({"result": result})





if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

