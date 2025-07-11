#!/bin/bash
set -e

# 1) Tuer l’API (Tuer tous les workers Gunicorn)
pkill -f "gunicorn: master" || true

# 2) Nettoyer l’ancien répertoire
rm -rf /home/ubuntu/API_DataLake/

# 3) Vider le cache APT
apt-get clean

# 4) Supprimer tous les logs système
rm -rf /var/log/*