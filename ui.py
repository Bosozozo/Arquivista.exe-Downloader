import os
import requests
from urllib.parse import unquote  # Pour décoder les caractères encodés comme %20
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QComboBox, QFileDialog, QProgressBar, QMessageBox
from PyQt5.QtCore import QThread, pyqtSignal
from downloader import list_files, download_files
from systems import get_systems

class Worker(QThread):
    progress = pyqtSignal(int, int)  # (current, total)
    download_finished = pyqtSignal(int, int)  # (downloaded_count, skipped_count)
    error = pyqtSignal(str)

    def __init__(self, files_to_download, download_folder):
        super().__init__()
        self.files_to_download = files_to_download
        self.download_folder = download_folder

    def run(self):
        downloaded_count, skipped_count = 0, 0
        total_files = len(self.files_to_download)

        for index, full_url in enumerate(self.files_to_download):
            # Décoder le nom du fichier pour enlever les %20, %2F, etc.
            decoded_file_name = unquote(full_url.split('/')[-1])
            file_name = os.path.join(self.download_folder, decoded_file_name)

            if os.path.exists(file_name):
                skipped_count += 1
            else:
                try:
                    # Télécharger le fichier
                    file_response = requests.get(full_url)
                    file_response.raise_for_status()
                    with open(file_name, 'wb') as f:
                        f.write(file_response.content)
                    downloaded_count += 1
                except Exception as e:
                    self.error.emit(f"Error downloading {decoded_file_name}: {str(e)}")
                    return

            self.progress.emit(index + 1, total_files)

        self.download_finished.emit(downloaded_count, skipped_count)


class DownloaderApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.system_label = QLabel('Select a system:')
        layout.addWidget(self.system_label)

        self.system_combo = QComboBox()
        self.system_combo.addItems(get_systems().keys())
        layout.addWidget(self.system_combo)

        self.filter_label = QLabel('Select a region:')
        layout.addWidget(self.filter_label)

        # Ajouter "ALL" comme option de filtre
        self.filter_combo = QComboBox()
        self.filter_combo.addItems(["ALL", "EU", "JP", "US", "WR", "DE", "ES", "FR", "GE", "IT"])
        layout.addWidget(self.filter_combo)

        self.download_button = QPushButton('Download')
        self.download_button.clicked.connect(self.on_download)
        layout.addWidget(self.download_button)

        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)

        self.progress_label = QLabel('Progress : 0/0')
        layout.addWidget(self.progress_label)

        self.setLayout(layout)
        self.setWindowTitle('Arquivista.exe Downloader')
        self.setGeometry(300, 300, 400, 200)

    def on_download(self):
        selected_system = self.system_combo.currentText()
        selected_filter = self.filter_combo.currentText()
        base_url = get_systems().get(selected_system, None)

        if not base_url:
            QMessageBox.warning(self, "Error", "Please select a system.")
            return

        # Si "ALL" est sélectionné, on récupère tous les fichiers sans appliquer de filtre
        if selected_filter == "ALL":
            files_to_download = list_files(base_url, None)  # None signifie pas de filtre
        else:
            files_to_download = list_files(base_url, selected_filter)

        if files_to_download is None or len(files_to_download) == 0:
            QMessageBox.warning(self, "No file found", f"No file including '{selected_filter}' has been found for {selected_system}.")
            return

        download_folder = QFileDialog.getExistingDirectory(self, "Select a folder")

        if not download_folder:
            QMessageBox.warning(self, "Error", "Please select a folder.")
            return

        self.worker = Worker(files_to_download, download_folder)
        self.worker.progress.connect(self.update_progress)
        self.worker.download_finished.connect(self.on_download_finished)
        self.worker.error.connect(self.handle_error)
        self.worker.start()

    def update_progress(self, current, total):
        self.progress_bar.setValue(current)
        self.progress_label.setText(f"Progress : {current}/{total}")
        self.progress_bar.setMaximum(total)

    def on_download_finished(self, downloaded_count, skipped_count):
        QMessageBox.information(self, "Done", f"Done : {downloaded_count} files downloaded, {skipped_count} skipped.")

    def handle_error(self, error_message):
        QMessageBox.critical(self, "Error", error_message)
