#!/bin/bash
set -e

# 1) Installer Python 3.12 & virtualenv
apt-get update -y
apt-get install -y software-properties-common
add-apt-repository -y ppa:deadsnakes/ppa
apt-get update -y
apt-get install -y python3.12 python3-virtualenv python3.12-distutils

# 2) Installer ton code
cd /home/ubuntu/API_DataLake/
virtualenv -p python3.12 env
. env/bin/activate
pip install --upgrade pip
pip install -r requirements-prod.txt

# 3) Lancer l’API en arrière-plan
nohup python app.py > start.out 2> start.err &