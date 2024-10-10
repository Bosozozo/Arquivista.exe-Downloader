# Arquivista.exe Downloader

## Description

Cette application permet de télécharger des fichiers depuis les URLs archivées d'Arquivista.exe sur le site archive.org, en filtrant les fichiers par région (`JP`, `EU`, `US`, etc.) et en les téléchargeant directement dans un dossier choisi par l'utilisateur. L'application dispose d'une interface graphique moderne construite avec **PyQt5** et inclut une barre de progression affichant l'avancement du téléchargement fichier par fichier.

## Fonctionnalités

- **Sélection de systèmes** : Choisissez un système parmi les options disponibles (ex. : PSX, Dreamcast, PSP, etc.).
- **Filtrage des fichiers** : Filtrez les fichiers en fonction de la région (`JP`, `EU`, `US`, ...).
- **Téléchargement dans un dossier** : Sélectionnez un dossier de destination où les fichiers seront téléchargés.
- **Barre de progression** : Suivez l'avancement du téléchargement via une barre de progression.
- **Affichage de la progression** : Le nombre de fichiers téléchargés et ignorés est affiché dans un label mis à jour en temps réel.
- **Gestion des erreurs** : Les erreurs de téléchargement ou de sélection sont affichées dans des boîtes de dialogue.

## Structure du projet

### 1. `main.py`

Ce fichier contient le point d'entrée principal de l'application. Il initialise l'application PyQt5 et affiche la fenêtre principale de l'interface utilisateur.

### 2. `downloader.py`

Ce fichier contient la logique principale de téléchargement :
- **`list_files(base_url, selected_filter)`** : Récupère la liste des fichiers disponibles sur une URL spécifique et filtre ceux qui correspondent à la région sélectionnée (`JP`, `EU`, etc.).
- **`download_files(download_folder, files_to_download, progress_callback)`** : Télécharge les fichiers dans le dossier sélectionné et met à jour la progression du téléchargement via un callback.

### 3. `ui.py`

Ce fichier gère l'interface utilisateur :
- Contient des widgets pour la sélection du système, du filtre de région, la sélection d'un dossier, une barre de progression, et un label d'avancement.
- Gère les événements utilisateurs comme la sélection d'un dossier et le clic sur le bouton de téléchargement.
- Appelle les fonctions définies dans `downloader.py` pour gérer le processus de téléchargement.

### 4. `systems.py`

Ce fichier stocke les configurations des systèmes disponibles et leurs URLs associées :
- **`systems_urls`** : Dictionnaire contenant les systèmes et leurs URLs.
- **`get_systems()`** : Renvoie la liste des systèmes disponibles et leurs URLs associées.

## Prérequis

- **Python 3.x**
- **PyQt5** pour l'interface graphique

Pour installer PyQt5, exécutez la commande suivante :

```bash
pip install PyQt5
```

## A savoir

Les téléchargement provenant du site archive.org, ils peuvent parfois être très lents.