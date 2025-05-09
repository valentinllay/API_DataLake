## Structure du dépôt

api-hello-world/
├── src/
│   └── hello_world/
│       ├── __init__.py
│       └── greet.py
├── tests/
│   └── test_greet.py
├── setup.py
├── pytest.ini
├── requirements.txt
├ - - venv/ (à créer soit même)
└── .github/
    └── workflows/
        └── main.yml

---

# Contenu des fichiers

### src/hello_world/greet.py

```python
def say_hello_world():
 return "Hello world !"
```

### src/hello_world/__init__.py

```python
# empty file
```

### tests/test_greet.py

```python
from hello_world.greet import say_hello_world

def test_say_hello_world():
 assert say_hello_world() == "Hello world !"
```

### setup.py

```python
from setuptools import setup, find_packages

setup(
 name="hello_world",
 version="0.1.0",
 packages=find_packages(where="src"),
 package_dir={"": "src"},
 install_requires=[
 # ajoute ici Flask si besoin, ex. "Flask>=2.2.5"
 ],
)
```

### pytest.ini

```actionscript
[pytest]
testpaths = tests
python_paths = src
```

### requirements.txt

```txt
pytest
Flask
spyder-kernels==2.5.*
```

## .github/workflows/main.yml

```yml
name: CI

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8]

    steps:
      - uses: actions/checkout@v3

      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}

      - name: Install deps
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install -e .

      - name: Run pytest
        run: pytest tests/
```

---

# Initialisation du venv local

L'objectif est de créer un espace virtuel local (venv) qui sera le même entre la phase de développement, de tests avec pytest et de production avec la machine sur AWS. 

Ouvre un terminal à la racine du projet (api-hello-world/) et exécute :

## Créer, activer le virtualenv, mettre à jour pip et installer les dépendances + package en editable

A executer une seule fois au début pour créer le (venv)

```cmd
python -m venv venv
venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
pip install -e .
```

- pip install -e . lie src/hello_world à ton environnement ; toute modification dans le code est immédiatement prise en compte.

- Pour lancer les tests localement dans le (venv) : 
  
  ```cmd
  pytest tests/
  ```

       ou bien il suffit de double cliquer sur `run_all_pytest_tests.bat`.

---

## Brancher hello_world à un script externe

Si tu veux utiliser ton package à partir d'un script  externe monscript.py dans ~/Downloads : 

```python
from hello_world.greet import say_hello_world

result = say_hello_world()
print(result)
```

1. Active le même venv (celui où tu as fait pip install -e .).
2. Dans le terminal, place-toi dans ~/Downloads (ou donne le chemin complet) et lance :
   python monscript.py
3. Le script importera hello_world.greet grâce au lien créé par -e ., même s’il est hors du projet.
