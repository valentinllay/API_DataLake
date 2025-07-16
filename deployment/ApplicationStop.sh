#!/bin/bash
# « fail fast » robuste
set -euo pipefail

# 1) Tuer brutalement l’API
pkill -f "python -m api.app" || true

# Libérer le port 5000
fuser -k 5000/tcp || true

# Le script renvoie 0 (succès) à la fin
exit 0 