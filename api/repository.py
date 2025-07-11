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

def fetch_latest_calcul_ltv(insee_code: str, age: int, borrower: str) -> Row | None:
    """
    Récupère la dernière entrée de calcul d'LTV pour un code INSEE, un âge 
    et un emprunteur donnés.

    Args:
        insee_code: Code INSEE du client.
        age: Âge du client.
        borrower: Identifiant de l’emprunteur.

    Returns:
        Un RowMapping contenant les colonnes de la ligne trouvée,
        ou None si aucun enregistrement ne correspond aux critères.
    """
    engine = create_db_engine()
    with engine.connect() as conn:
        query = text(
            """
            SELECT *
            FROM calculs_ltv
            WHERE insee_code = :insee_code
              AND age = :age
              AND borrower = :borrower
            ORDER BY id DESC
            LIMIT 1
            """
        )
        result = conn.execute(query, {
            'insee_code': insee_code,
            'age': age,
            'borrower': borrower
        })
        return result.fetchone()