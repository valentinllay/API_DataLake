#!/bin/bash
set -e

# 1) Installer Python & venv
apt-get update -y
apt-get install -y software-properties-common
add-apt-repository -y ppa:deadsnakes/ppa
apt-get install -y python3.8 python3.8-venv python3.8-distutils

# 2) Créer & activer venv
cd /home/ubuntu/API_DataLake/ || { echo "Dossier introuvable"; exit 1; }
python3.8 -m venv env
. env/bin/activate
pip install --upgrade pip
pip install -r requirements-prod.txt

# 3) Lancer l’API, logs séparés (standard outputs et erreurs)
nohup python app.py > start.out 2> start.err &