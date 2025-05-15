#!/bin/bash
set -e

# 1) Installer Python & venv
apt-get update -y
apt-get install -y python3 python3-venv python3-distutils

# 2) Créer & activer venv
cd /home/ubuntu/API_DataLake/ || { echo "Dossier introuvable"; exit 1; }
python3 -m venv env
. env/bin/activate
pip install --upgrade pip
pip install -r requirements-prod.txt

# 3) Lancer l’API, logs séparés (standard outputs et erreurs)
nohup python app.py > start.out 2> start.err &