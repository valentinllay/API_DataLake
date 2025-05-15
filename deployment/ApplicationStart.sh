#!/bin/bash
set -e

# 1) Installer Python & venv
apt-get update -y
apt-get install -y python3.12 python3.12-venv

# 2) Créer & activer venv
cd /home/ubuntu/API_DataLake/ || { echo "Dossier introuvable"; exit 1; }
rm -rf env
python3.12 -m venv env
. env/bin/activate
python -m pip install --upgrade pip
pip install -r requirements-prod.txt

# 3) Lancer l’API, logs séparés (standard outputs et erreurs)
nohup python app.py > start.out 2> start.err &