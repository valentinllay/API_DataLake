### ApplicationStart.sh

##### Avant

```shell
#!/bin/bash

# 1) Installer Python 3.8 & virtualenv
apt-get update -y
apt-get install -y software-properties-common
add-apt-repository -y ppa:deadsnakes/ppa
apt-get update -y
apt-get install -y python3.8 python3-virtualenv python3.8-distutils

# 2) Installer ton code
cd /home/ubuntu/API_DataLake/
virtualenv -p python3.8 env
. env/bin/activate
pip install --upgrade pip
pip install -r requirements-prod.txt

# 3) Lancer l’API en arrière-plan
nohup python app.py > /home/ubuntu/API_DataLake/nohup.log 2>&1 &
```

##### Après

```shell
#!/bin/bash
set -e

# 1) Installer Python & venv
apt-get update -y
apt-get install -y python3.12 python3.12-venv

# 2) Créer & activer venv
cd /home/ubuntu/API_DataLake/ || { echo "Dossier introuvable"; exit 1; }
rm -rf env
python3.12 -m venv env
. env/bin/activate
python -m pip install --upgrade pip
pip install -r requirements-prod.txt

# 3) Lancer l’API, logs séparés (standard outputs et erreurs)
nohup python app.py > start.out 2> start.err &
```

Améliroations : 

- `set -e` permet de faire cracher tout le script si une ligne renvoie une erreur plutot que de poursuivre l'execution.

- Passage à `Python 3.12`.

- Passage de `virtualenv` à `venv`.

- Suppression de `software-properties-common`  et `PPA deadsnakes` car depuis Ubuntu 24.04, **Python 3.12** et son module `venv` sont déjà dans les dépôts officiels. Inutile de rajouter une PPA externe.

- Supression de `python3.12-distutils` car n'existe plus.

### ApplicationStop.sh

##### Avant

```shell
#!/bin/bash

# 1) Tuer l’API sur le port 5000
lsof -ti :5000 | xargs --no-run-if-empty kill -9

# 2) Optionnel : nettoyer l’ancien répertoire
rm -rf /home/ubuntu/API_DataLake/
```

##### Après

```shell
#!/bin/bash
set -e

# 1) Tuer l’API 
pkill -f "python app.py" || true

# 2) Nettoyer l’ancien répertoire
rm -rf /home/ubuntu/API_DataLake/

# 3) Vider le cache APT
apt-get clean

# 4) Supprimer tous les logs système
rm -rf /var/log/*
```

**`pkill -f "python app.py"` vs `lsof | kill -9`**

- `pkill -f "python app.py"` utilise la recherche par nom de commande ; c’est simple, lisible et ne dépend pas de l’installation de `lsof`.

- L’approche `lsof -ti :5000 | xargs kill -9` cible uniquement le port 5000, mais :
  
  1. Le flag `-9` fait un **kill brutal**, sans laisser l’application fermer proprement.
  
  2. `lsof` n’est pas toujours installé par défaut sur toutes les AMI.

- Avec `pkill -f` et `|| true`, tu t’assures que le script ne plante pas si le process a déjà disparu, et tu laisses l’application se terminer avec un **signal TERM** par défaut, un peu plus propre.

- Nettoyage à chaque déploiement avec `apt-get clean` et `rm -rf /var/log/*`

### User Data (instance EC2)

##### Avant

```shell
#!/bin/bash
set -e

# 1) Update package lists
apt-get update -y

# 2) Install agent prerequisites
apt-get install -y ruby-full wget

# 3) Download & install CodeDeploy agent
cd /home/ubuntu
wget https://aws-codedeploy-eu-west-3.s3.eu-west-3.amazonaws.com/latest/install
chmod +x install
./install auto > /tmp/logfile

# 4) Verify the agent is running
systemctl status codedeploy-agent --no-pager
```

##### Après

```shell
#!/bin/bash
set -e

# 1) Update package lists
apt-get update -y

# 2) Install agent prerequisites
apt-get install -y ruby-full wget

# 3) Download & install CodeDeploy agent
cd /home/ubuntu
wget https://aws-codedeploy-eu-west-3.s3.eu-west-3.amazonaws.com/latest/install
chmod +x install
./install auto > /tmp/codedeploy-install.log 2>&1

# 4) Verify the agent is running
systemctl status codedeploy-agent --no-pager
```
