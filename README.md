## Structure du dépôt

API_DataLake/
│
├── config.py                  # Configuration centrale (LOG_LEVEL, formats…)
├── db.py                      # Factory create_db_engine()
├── repository.py              # Fonctions SQL brutes
├── services.py                # Orchestration & logique métier
├── validators.py              # Validation des payloads
├── security.py                # Décorateurs d’authentification
├── errors/                    # Exceptions métiers et handlers
│   └── exceptions.py
│
├── api/                       # Couche HTTP
│   └── app.py                 # Flask app, routes, errorhandlers, hooks
│
├── comparateur/               # Package métier “comparateur”
│   └── report.py
│
├── hello_world/               # Package métier “hello_world”
│   └── greetings.py
│
├── reversemortgage/           # Package métier “reverse mortgage”
│   └── report_simplified.py
│
├── viager/                    # Package métier “viager”
│   └── calculator.py
│
├── scripts/                   # Scripts divers
│   ├── python/                
│   │   └── benchmark.py
│   └── bat/                   
│       └── run_benchmark.bat
│
├── deployment/                # Scripts de déploiement
│   ├── ApplicationStart.sh
│   ├── ApplicationStop.sh
│   └── check_modes.bat
│
├── tests/                     # Tests pytest
│   ├── api/
│   ├── comparateur/
│   ├── hello_world/
│   ├── reversemortgage/
│   └── viager/
│
├── requirements-dev.txt
├── requirements-prod.txt
└── README.md

---

# Contenu des fichiers

### hello_world/greet.py

```python
def say_hello_world():
 return "Hello world !"
```

### tests/test_greet.py

```python
from hello_world.greet import say_hello_world

def test_say_hello_world():
 assert say_hello_world() == "Hello world !"
```

## appspecs.yml

**Explication courte**

- **files** : copie tout le contenu du ZIP (ton repo) sous `/home/ubuntu/API_DataLake/`.

- **hooks** : arrête à l’ancienne puis démarre ta nouvelle version via tes scripts.

## .deployment/ApplicationStart.sh

## .deployment/ApplicationStop.sh

Attention il faut rendre ApplicationStart.sh et ApplicationStop executables avant de push dans github en faisant : `chmod +x ApplicationStart.sh ApplicationStop.sh`

---

# Initialisation du venv-dev local

L'objectif est de créer un espace virtuel local (venv) qui sera le même entre la phase de développement, de tests avec pytest et de production avec la machine sur AWS.

Ouvre un terminal à la racine du projet (api-hello-world/) et exécute :

## Créer, activer le virtualenv, mettre à jour pip et installer les dépendances + package en editable

A executer une seule fois au début pour créer le (venv-dev)

```cmd
python -m venv venv-dev
venv-dev\Scripts\activate
pip install --upgrade pip
pip install -r requirements-dev.txt
```

- pip install -e . lie src/hello_world à ton environnement ; toute modification dans le code est immédiatement prise en compte.

- Pour lancer tests localement dans le (venv-dev) :
  
  ```cmd
  pytest tests/
  ```

       ou bien il suffit de double cliquer sur `run_all_pytest_tests.bat`.
       pour executer un seul test il suffit de faire : 

```cmd
pytest tests/test_greet.py::test_say_hello_world
```

---

## Brancher hello_world à un script externe

Si tu veux utiliser ton package à partir d'un script externe monscript.py dans ~/Downloads :

```python
from hello_world.greet import say_hello_world

result = say_hello_world()
print(result)
```

1. Active le même venv-dev.
2. Dans le terminal, place-toi dans ~/Downloads (ou donne le chemin complet) et lance :
   python monscript.py
3. Le script importera hello_world.greet grâce au lien créé par -e ., même s’il est hors du projet.
