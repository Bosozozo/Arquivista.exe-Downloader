import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, unquote
import os

def list_files(base_url, selected_filter):
    """Liste les fichiers correspondant au filtre dans l'URL donnée."""
    try:
        response = requests.get(base_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            links = soup.find_all('a', href=True)
            # Filtrer les liens contenant le filtre sélectionné
            return [urljoin(base_url + '/', link['href']) for link in links if selected_filter in link['href']]
        else:
            return None
    except requests.exceptions.RequestException as e:
        return None

def download_files(download_folder, files_to_download, progress_callback):
    """Télécharge les fichiers dans le dossier sélectionné."""
    total_files = len(files_to_download)
    downloaded_count = 0
    skipped_count = 0

    for index, full_url in enumerate(files_to_download):
        file_name = os.path.join(download_folder, unquote(full_url.split('/')[-1]))

        # Vérification si le fichier existe déjà
        if os.path.exists(file_name):
            print(f"Skipped : {file_name} already exists.")
            skipped_count += 1
        else:
            try:
                file_response = requests.get(full_url)
                file_response.raise_for_status()
                with open(file_name, 'wb') as f:
                    f.write(file_response.content)
                print(f"Downloaded : {file_name}")
                downloaded_count += 1
            except Exception as e:
                print(f"Error during download : {e}")

        # Mise à jour de la progression via le callback
        progress_callback(index + 1, total_files)

    return downloaded_count, skipped_count
