@echo off
REM — Se placer dans le dossier contenant ce script
cd /d "%~dp0"

REM — Remonter de deux dossiers (depuis API_DataLake\deployment ou scripts\python)
cd ..\..

REM — Activer l'environnement virtuel
call venv-3.10.8\Scripts\activate.bat

REM — Lancer le benchmark
python scripts\python\benchmark.py

REM — Garder la fenêtre ouverte pour voir les résultats
cmd /k
