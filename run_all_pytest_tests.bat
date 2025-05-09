@echo off
REM Vérifier que le venv existe
if not exist "venv\Scripts\activate" (
    echo Virtual environment not found.
    echo Please create and set up your venv by running these commands:
    echo.
    echo     python -m venv venv
    echo     venv\Scripts\activate
    echo     pip install --upgrade pip
    echo     pip install -r requirements.txt
    echo     pip install -e .
    echo.
    pause
    exit /b 1
)

REM Activer le venv
call venv\Scripts\activate

REM Lancer les tests
echo Running pytest tests...
pytest tests/

cmd /k
