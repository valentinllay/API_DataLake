@echo off
REM — Recule de deux niveaux
cd ..\..
 
REM — Active l'environnement virtuel
call venv-3.10.8\Scripts\activate.bat

REM — Lance l’API Flask
python app.py

REM — Facultatif : garde la fenêtre ouverte pour voir les logs
pause
