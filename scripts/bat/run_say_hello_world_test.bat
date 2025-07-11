@echo off

REM Move back one level up to the project root
cd ..
REM Move back one level up to the project root
cd ..


REM Vérifier que le venv-dev existe
if not exist "venv-3.10.8\Scripts\activate" (
    echo Virtual environment not found.
    echo Please create and set up your venv by running these commands:
    echo.
    echo     python -m venv venv-dev
    echo     venv-dev\Scripts\activate
    echo     pip install --upgrade pip
    echo     pip install -r requirements-dev.txt
    echo.
    pause
    exit /b 1
)

REM Activer le venv
call venv-3.10.8\Scripts\activate

REM Lancer les tests
echo Running pytest tests...
pytest tests/test_greet.py::test_say_hello_world -vv

cmd /k
