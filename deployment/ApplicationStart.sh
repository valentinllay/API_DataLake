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

# 3) Lancer l’API, logs séparés : appels HTTP (access.log), infos (gunicorn.out), erreurs critiques (gunicorn.err)
nohup env/bin/gunicorn \
  -w 4 -k gthread \
  -b 0.0.0.0:5000 \
  api.app:app \
  --access-logfile access.log \
  > gunicorn.out 2> gunicorn.err &