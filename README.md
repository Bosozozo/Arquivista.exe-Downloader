
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
