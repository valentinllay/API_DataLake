#!/bin/bash
set -e

# 1) Installer Python & venv
apt-get update -y
apt-get install -y \
    python3.12 \
    python3.12-venv \
    python3.12-dev \
    build-essential \
    libssl-dev \
    libffi-dev

# 2) Créer & activer venv
cd /home/ubuntu/API_DataLake/ || { echo "Dossier introuvable"; exit 1; }
rm -rf env
python3.12 -m venv env
. env/bin/activate
python -m ensurepip --upgrade
pip install --upgrade pip setuptools
pip install -r requirements-prod.txt

# 3) Lancer l’API, logs séparés (standard outputs et erreurs)
nohup python app.py > start.out 2> start.err &