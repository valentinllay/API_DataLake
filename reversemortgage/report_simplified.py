import datetime

import reversemortgage.report


class InputValidationError(Exception):
    """
    Erreur levée quand les inputs sont invalides.
    Sert à distinguer une erreur lié à l'intput user d'une erreur interne de calcul de LTV.
    """
    pass


def get_todays_date_iso() -> str:
    """
    Retourne la date du jour au format ISO 'YYYY-MM-DD'.
    """
    return datetime.date.today().isoformat()


def calcul_date_naissance(age: int) -> str:
    """
    Calcule une date de naissance au format 'YYYY-MM-DD' à partir d’un âge (en années).
    On reprend le mois et le jour d’aujourd’hui, en soustrayant l’âge en années.
    En cas de 29 février et d’année non-bissextile, on bascule au 28 février.
    """
    today = datetime.date.today()
    try:
        naissance = today.replace(year=today.year - age)
    except ValueError:
        # Cas du 29 février pour une année non-bissextile
        naissance = datetime .date(today.year - age, 2, 28)
    # Retire toujours un jour juste pour être sûr
    naissance = naissance - datetime.timedelta(days=1)
    return naissance.isoformat()


def construct_borrowers(inputs: dict) -> list:
    borrowers = [{
        "birth_date": calcul_date_naissance(inputs["age_1"]),
        "gender": inputs["gender_1"],
        "income_quantile": 11,
        "alive": True
    }]
    if inputs["gender_2"] is not None:
        borrowers.append({
            "birth_date": calcul_date_naissance(inputs["age_2"]),
            "gender": inputs["gender_2"],
            "income_quantile": 11,
            "alive": True
        })
    return borrowers


def get_default_inputs_complets():
    """
    Inputs par défaut.
    """
    inputs_complets = {
      "calculation_parameters": {
        "calculation_date": None,
        "calculation_mode": 1,
        "expected_loss_to_fail_scenario": 0,
        "annual_time_steps": 1,
        "projection_years": 60,
        "mortality_diversification": True,
        "global_scenarios": [
          0
        ],
        "loss_quantile_to_use": -1,
        "discount_losses": True,
        "verbose": True,
        "pricing_method": "advanced"
      },
      "borrowers": [],
      "collateral_asset": {
        "real_estate_type": None, # A CHANGER
        "last_price_estimation_date": "2024-10-10",
        "last_price_estimation": 300_000,
        "insee_code": None, # A CHANGER
        "type_bien": "Résidence principale"
      },
      "loan_terms": {
        "already_issued": False,
        "issue_date": "2099-01-01",
        "initial_outstanding": 1,
        "grace_period": 0.25,
        "levier_taux_variable": 0,
        "quotity": None,
        "bank": "ARRAGO"
      },
      "liability_financing": {
        "already_issued": False,
        "issue_date": "2099-01-01",
        "levier_taux_variable": 0,
        "initial_outstanding": 0
      }
    }

    return inputs_complets



def validate_inputs(inputs: dict) -> None:
    """
    Verifie la coherence et la validite brute des inputs pour le calcul de LTV simplifie.
    Lève InputValidationError des qu’un champ manque ou n’appartient pas aux valeurs autorisees.
    - real_estate_type : doit etre '1','2','Appartement' ou 'Maison'
    - insee_code       : 4 ou 5 chiffres
    - gender_1         : '1','2','Homme' ou 'Femme'
    - age_1            : entier entre 60 et 122
    - gender_2, age_2  : optionnels, mais doivent etre fournis ensemble
    """
    # 1) presence et non-vide des champs obligatoires
    for f in ("real_estate_type", "insee_code", "gender_1", "age_1"):
        if f not in inputs or inputs[f] is None or (isinstance(inputs[f], str) and inputs[f].strip() == ""):
            raise InputValidationError(f"parametre '{f}' requis et non vide")

    # 2) real_estate_type brut
    rt = str(inputs["real_estate_type"]).strip().lower()
    if rt not in ("1", "2", "appartement", "maison"):
        raise InputValidationError(
            f"real_estate_type invalide: valeurs autorisees ['1','2','Appartement','Maison'], recu '{inputs['real_estate_type']}'"
        )

    # 3) insee_code brut
    ic = str(inputs["insee_code"]).strip()
    if not ic.isdigit() or not (4 <= len(ic) <= 5):
        raise InputValidationError(
            f"insee_code invalide: doit contenir 4 ou 5 chiffres, recu '{inputs['insee_code']}'"
        )

    # 4) gender_1 brut
    g1 = str(inputs["gender_1"]).strip().lower()
    if g1 not in ("1", "2", "homme", "femme"):
        raise InputValidationError(
            f"gender_1 invalide: valeurs autorisees ['1','2','Homme','Femme'], recu '{inputs['gender_1']}'"
        )

    # 5) age_1 brut
    try:
        a1 = int(inputs["age_1"])
    except (TypeError, ValueError):
        raise InputValidationError("age_1 invalide: doit etre un entier")
    if not (60 <= a1 <= 122):
        raise InputValidationError(
            f"age_1 invalide: doit etre compris entre 60 et 122, recu {a1}"
        )

    # 6) duo optionnel gender_2/age_2
    has_g2 = "gender_2" in inputs and inputs["gender_2"] not in (None, "")
    has_a2 = "age_2"   in inputs and inputs["age_2"]   not in (None, "")
    if has_g2 ^ has_a2:
        raise InputValidationError("gender_2 et age_2 doivent etre fournis ensemble")
    if has_g2:
        g2 = str(inputs["gender_2"]).strip().lower()
        if g2 not in ("1", "2", "homme", "femme"):
            raise InputValidationError(
                f"gender_2 invalide: valeurs autorisees ['1','2','Homme','Femme'], recu '{inputs['gender_2']}'"
            )
        try:
            a2 = int(inputs["age_2"])
        except (TypeError, ValueError):
            raise InputValidationError("age_2 invalide: doit etre un entier")
        if not (60 <= a2 <= 122):
            raise InputValidationError(
                f"age_2 invalide: doit etre compris entre 60 et 122, recu {a2}"
            )



def normalize_inputs(inputs: dict) -> None:
    """
    Transforme in-place les valeurs validées en types finaux :
    - real_estate_type → int (1=appartement,2=maison)
    - insee_code       → str de 5 chiffres (pad zero)
    - gender_1, gender_2 → int (1=Homme,2=Femme)
    - age_1, age_2       → int
      Si gender_2/age_2 absents, on fixe inputs[...] = None
    """
    # real_estate_type
    raw_rt = str(inputs["real_estate_type"]).strip().lower()
    inputs["real_estate_type"] = 1 if raw_rt in ("appartement", "1") else 2

    # insee_code → 5 chiffres
    ic = str(inputs["insee_code"]).strip()
    inputs["insee_code"] = f"{int(ic):05d}"

    # gender_1 → 1 ou 2
    raw_g1 = str(inputs["gender_1"]).strip().lower()
    inputs["gender_1"] = 1 if raw_g1 in ("1", "homme") else 2

    # age_1
    inputs["age_1"] = int(inputs["age_1"])

    # gender_2 & age_2
    if inputs.get("gender_2") in (None, ""):
        inputs["gender_2"] = None
        inputs["age_2"]    = None
    else:
        raw_g2 = str(inputs["gender_2"]).strip().lower()
        inputs["gender_2"] = 1 if raw_g2 in ("1", "homme") else 2
        inputs["age_2"]    = int(inputs["age_2"])



def build_report(inputs: dict) -> dict:
    """
    Construction de l'input complet à partir d'inputs simplifiés.
    Simplifie les résultats du calcul de LTV pour masquer tous les détails du calculateur.
    """
    validate_inputs(inputs)
    normalize_inputs(inputs)

    # construction de l'input complet
    inputs_complets = get_default_inputs_complets()
    inputs_complets["calculation_parameters"]["calculation_date"] = get_todays_date_iso()
    inputs_complets["borrowers"] = construct_borrowers(inputs)
    inputs_complets["collateral_asset"]["real_estate_type"] = inputs["real_estate_type"]
    inputs_complets["collateral_asset"]["insee_code"] = inputs["insee_code"]

    # calcul LTV complet
    results = reversemortgage.report.build_report(inputs_complets)

    # sortie simplifiée
    return {
        "ltv":     results["Base Case"]["maximum_quotity"],
        "prix_5%": results["Base Case"]["Quantile_Prix_Immo"]["prix 5%"]
    }



if __name__ == "__main__":
    inputs = {
        "real_estate_type": 2, # 1, 2 ou "Maison", "Appartement"
        "insee_code": "83137",
        "gender_1": 2,
        "age_1": 65,
        "gender_2": None,
        "age_2": None
    }

    build_report(inputs)
    response_simplified = build_report(inputs)
    print(response_simplified)