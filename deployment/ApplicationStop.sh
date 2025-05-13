#!/bin/bash
set -e

# 1) Tuer l’API sur le port 5000
lsof -ti :5000 | xargs --no-run-if-empty kill -9

# 2) Optionnel : nettoyer l’ancien répertoire
rm -rf /home/ubuntu/API_DataLake/