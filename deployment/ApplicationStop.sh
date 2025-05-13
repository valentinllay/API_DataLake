#!/bin/bash
set -e

# 1) Tuer l’API 
pkill -f "python app.py" || true

# 2) Nettoyer l’ancien répertoire
rm -rf /home/ubuntu/API_DataLake/