"""
Script de test pour valider le rate-limit IP sur l'endpoint /v1/maximum_quotity.
Ce script envoie plusieurs requêtes successives et affiche les codes de statut reçus.
"""
import time
import requests
import sys

# Configuration
BASE_URL = "http://13.36.203.126:5000"
# BASE_URL = "http://localhost:5000"
ENDPOINT = "/v1/maximum_quotity"
FULL_URL = f"{BASE_URL}{ENDPOINT}"

# Payload minimal pour l'appel (ajuster si besoin)
PAYLOAD = {
    "insee_code": "75110",
    "user_email": "test@example.com",
    "age_1": 60,
    "gender_1": 1,
    "borrower_type": "homme_seul",
    "real_estate_type": 1
}

# Nombre de requêtes à envoyer (ex: 730 pour dépasser le quota 720/min)
N_REQUESTS = 730
# Pause entre les requêtes (en secondes)
DELAY = 0

status_counts = {}

for i in range(1, N_REQUESTS + 1):
    try:
        resp = requests.post(FULL_URL, json=PAYLOAD)
        code = resp.status_code
    except Exception as e:
        code = f"ERR: {e}"
    print(f"Request {i}: status {code}")
    status_counts[code] = status_counts.get(code, 0) + 1
    time.sleep(DELAY)

print("\nRésumé des codes reçus :")
for code, count in status_counts.items():
    print(f"  {code} -> {count} fois")

if __name__ == "__main__":
    # Exécution directe
    print(f"Lancement du test rate limit: {N_REQUESTS} requêtes à {FULL_URL}")
    # Le corps principal s'exécute automatiquement
    sys.exit(0)