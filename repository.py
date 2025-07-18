"""
repository.py

Contient les fonctions d’accès direct à la base (SQL brut), utilisant SQLAlchemy Core
et la factory `create_db_engine()` (qui sert à récupérer un engine pour les connexions).
Toutes les fonctions ici :
- "fetchent" la data filtrée ou non sur la base de données.
- Renvoient soit :
    -> Row : un objet RowMapping (ou Row) pour une seule ligne,
    -> list[Row] : une liste d'objets RowMapping pour plusieurs lignes,
    -> ou un scalaire si la requête renvoie exactement une valeur (compte, somme, etc.).
Le post-traitement de cette data est uniquement réservé aux fonctions de services.py qui
contient la logique métier
"""

from sqlalchemy import text
from sqlalchemy.engine import Row
from db import create_db_engine


def fetch_maximum_quotity(
    age_1: int,
    gender_1: int,
    borrower_type: str,
    insee_code: str,
    real_estate_type: str,
    age_2: int | None = None,
    gender_2: int | None = None,
) -> float | None:
    """
    Récupère la maximum_quotity pour les filtres donnés,
    en prenant d’abord la date de calcul la plus récente,
    puis l'enregistrement au plus grand id si plusieurs sur la même date.
    """
    engine = create_db_engine()
    with engine.connect() as conn:
        sql = """
        SELECT maximum_quotity
        FROM calculs_ltv_pour_grille_outil_excel
        WHERE insee_code       = :insee_code
          AND borrower_type    = :borrower_type
          AND real_estate_type = :real_estate_type
          AND age_1            = :age_1
          AND gender_1         = :gender_1
        """
        params: dict[str, object] = {
            "insee_code": insee_code,
            "borrower_type": borrower_type,
            "real_estate_type": real_estate_type,
            "age_1": age_1,
            "gender_1": gender_1,
        }

        if age_2 is None:
            sql += " AND age_2 IS NULL"
        else:
            sql += " AND age_2 = :age_2"
            params["age_2"] = age_2
        if gender_2 is None:
            sql += " AND gender_2 IS NULL"
        else:
            sql += " AND gender_2 = :gender_2"
            params["gender_2"] = gender_2

        # On prend d'abord la date la plus récente, puis l'id max
        sql += " ORDER BY calculation_date DESC, id DESC LIMIT 1"

        query = text(sql)
        result = conn.execute(query, params).mappings()
        row = result.fetchone()
        return row["maximum_quotity"] if row else None