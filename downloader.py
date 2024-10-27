import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, unquote
import os

def is_valid_file(link, file_extensions):
    """Vérifie si un lien correspond à un fichier valide basé sur ses extensions.
    Ignore les liens sans extension ou contenant des paramètres."""
    # Ignorer les liens contenant des paramètres (par exemple : ?origin=iawww-mbhrt)
    if "?" in link or "=" in link:
        return False

    # Vérifier si le lien contient un point (.) indiquant une extension et se termine par une extension valide
    if file_extensions:
        return any(link.lower().endswith(ext) for ext in file_extensions)
    
    # Si aucune extension n'est spécifiée, ne pas accepter de fichiers sans extension
    return '.' in link  # Filtrer les fichiers qui ont au moins un point

def list_files(base_url, selected_filter, file_extensions=None):
    """Liste les fichiers correspondant au filtre dans l'URL donnée.
    Si selected_filter est None, tous les fichiers sont retournés.
    file_extensions permet de filtrer par extension (ex: ['.zip', '.iso'])."""
    try:
        response = requests.get(base_url)
        response.raise_for_status()  # Assure que la requête a réussi
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a', href=True)

        # Si selected_filter est None, on renvoie tous les fichiers sans filtrer
        if selected_filter is None:
            files = [urljoin(base_url + '/', link['href']) for link in links if is_valid_file(link['href'], file_extensions)]
        else:
            # Sinon, on applique le filtre par région et on vérifie la validité des fichiers
            files = [urljoin(base_url + '/', link['href']) for link in links if selected_filter in link['href'] and is_valid_file(link['href'], file_extensions)]

        return files
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching files from {base_url}: {str(e)}")
        return None

def download_files(download_folder, files_to_download, progress_callback):
    """Télécharge les fichiers dans le dossier sélectionné."""
    total_files = len(files_to_download)
    downloaded_count = 0
    skipped_count = 0

    for index, full_url in enumerate(files_to_download):
        # Décoder l'URL pour enlever les caractères encodés
        file_name = os.path.join(download_folder, unquote(full_url.split('/')[-1]))

        # Vérification si le fichier existe déjà
        if os.path.exists(file_name):
            print(f"Skipped : {file_name} already exists.")
            skipped_count += 1
        else:
            try:
                # Télécharger le fichier
                file_response = requests.get(full_url)
                file_response.raise_for_status()  # Assure que la requête a réussi
                with open(file_name, 'wb') as f:
                    f.write(file_response.content)
                print(f"Downloaded : {file_name}")
                downloaded_count += 1
            except Exception as e:
                print(f"Error during download : {e}")

        # Mise à jour de la progression via le callback
        progress_callback(index + 1, total_files)

    return downloaded_count, skipped_count
