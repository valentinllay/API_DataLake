# Agrandissement d'un volume EBS - type Nitro

##### Uniqument sur EC2 Ubuntu avec plateforme de virtualisation "Nitro" (cas de API_Reverse_mortgage)

## Introduction

Ce guide explique comment étendre dynamiquement un volume EBS de 8 GiB à 16 GiB sur une instance EC2 AWS, puis comment redimensionner la partition et le système de fichiers sous Ubuntu sans interruption de service.

Ce document reprend les informations dans le guide aws (suivre les Nitro instance example) :

https://docs.aws.amazon.com/ebs/latest/userguide/recognize-expanded-volume-linux.html?icmpid=docs_ec2_console

## 1. Faire un snapshot de sauvegarde du volume EBS

1. Dans la console AWS, allez dans **Services → EC2 → Volumes**.

2. Cliquez sur **Actions → Create snapshot**.

## 2. Dans les paramètres EC2

1. Ouvrez la console AWS et naviguez vers **EC2**.

2. Dans le menu latéral, cliquez sur **Volumes** pour afficher la liste des disques associés à vos instances.

3. Sélectionnez le volume à agrandir (ex. `vol-0b58…`).

4. Dans **Actions → Modify Volume**, choisissez **Modify Volume**.

5. Changez **Size** de `8` à `16` (ou plus si besoin), puis cliquez sur **Modify**.

6. Attendez l’état **in-use (optimized)** : AWS procède en arrière-plan sans arrêter l’instance.

## 3. Dans l’instance EC2 Ubuntu Dans l’instance EC2 Ubuntu (étendre la partition et redimensionner le système de fichiers)

### Connexion à l'instance EC2

Connectez-vous à votre instance sur le site web AWS dès que le volume est en état **in-use (optimized)**.

### Afficher l'espace utilisé avant l'opération

```shell
df -h
```

```
ubuntu@ip-172-31-47-95:~$ df -h
Filesystem      Size  Used Avail Use% Mounted on
/dev/root       7.7G  6.1G  1.7G  79%  /
...
```

Le disque principal est plein à 79%. En étendant la partition principale et en redimensionnant le système de fichiers, ce pourcentage augmentera.

### Visualiser tous les disques et leurs partitions

```shell
lsblk
```

```
ubuntu@ip-172-31-47-95:~$ lsblk
NAME        MAJ:MIN RM SIZE RO TYPE MOUNTPOINT
nvme0n1     259:0    0  16G  0 disk 
└─nvme0n1p1 259:1    0   8G  0 part /
```

Vous devriez voir le disque principal `/nvme0` passer de 8 GiB à désormais 16 GiB comme dans l'exemple, tandis que la partition `nvme0n1p1` est encore à 8GiB car il faut encore l'étendre et redimensionner le système de fichiers. 

### Étendre la partition principale

```shell
sudo growpart /dev/nvme0n1 1
```

```
ubuntu@ip-10-0-1-21:~$ sudo growpart /dev/nvme0n1 1
CHANGED: partition=1 start=2099200 old: size=14677983 end=16777182 new: size=16775135 end=18874334
```

Cette commande étend la partition principale n° `1` pour occuper tout l’espace disponible. Si on vérifie la taille du disque avec la commande `lsblk` on devrait voir la ligne`└─nvme0n1p1` augmenter en taille.

**Astuce** : 

- si la commande `growpart` n’est pas disponible, installez le paquet `cloud-guest-utils` : `sudo apt update && sudo apt install -y cloud-guest-utils`. Puis relancez `growpart`.

### Redimensionner le système de fichiers

Avant, il faut vérifier le type de système de fichiers :

```shell
lsblk -f
```

```
ubuntu@ip-172-31-47-95:~$ lsblk -f
NAME        FSTYPE LABEL           UUID             FSAVAIL FSUSE% MOUNTPOINT
nvme0n1                                                           
└─nvme0n1p1 ext4   cloudimg-rootfs e8070c3...c23486    1.7G    78% /
```

Assurez-vous que le système de fichiers est **ext4**. Dans l'exemple, la partition principale `nvme0n1` du volumen principal `nvme0n1p1` a un File System Type `ext4` donc c'est le bon type pour la suite. Si c'est un autre type, demander à ChatGPT.

**Si votre système de fichiers est ext4** (Généralement le cas) :

```shell
sudo resize2fs /dev/nvme0n1p1
```

### Vérification finale

```shell
lsblk
```

```
ubuntu@ip-172-31-47-95:~$ lsblk
NAME        MAJ:MIN RM SIZE RO TYPE MOUNTPOINT
nvme0n1     259:0    0  16G  0 disk 
└─nvme0n1p1 259:1    0  16G  0 part /
```

La sortie doit maintenant afficher environ `16G` pour la partition racine `/`.

## Conclusion

Vous avez désormais agrandi votre volume EBS de 8 GiB à 16GiB sans interruption de service, et votre instance Ubuntu reconnaît la nouvelle taille du système de fichiers.
