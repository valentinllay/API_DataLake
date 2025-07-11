@echo off
REM Recule de deux niveaux
cd /d "%~dp0..\.."
 
REM Active l'environnement virtuel
call venv-3.10.8\Scripts\activate.bat

REM Garde la fenêtre ouverte
cmd /k
