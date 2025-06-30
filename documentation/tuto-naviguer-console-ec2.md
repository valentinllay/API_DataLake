# Comment naviguer dans la console de la machine EC2 ?

## Instruction cd

cd API_DataLake/ : permet d'acceder au répertoire API_DataLake
cd var/ : Ne marche pas car var/ n'existe pas dans le répertoire courant
cd /var/ : fonctionne car on précise le chemin absolue à partir de la racine du systeme.
cd : permet de revenir au répertoire courant /home/ubuntu
cd .. : permet de revenir en arrière

## Logs ApplicationStart.sh et ApplicationStop.sh

Voir les logs en temps réél sur la console au moment du déploiment :

```shell
cat /opt/codedeploy-agent/deployment-root/deployment-logs/codedeploy-agent-deployments.log
```

Voir les logs après coup d'un déploiment particulier :

```shell
cd /opt/codedeploy-agent/deployment-root/6c717fd5-7e4c-44d4-a934-88f9cee9e1b2/<ID-Deployment>
```

6c717fd5-7e4c-44d4-a934-88f9cee9e1b2 : c'est l'UUID du Deployment Group (API_DataLake-Prod-DG)
\<ID-Deployment> : exemple d-0TU402HHA
