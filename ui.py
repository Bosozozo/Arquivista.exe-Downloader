from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QComboBox, QFileDialog, QProgressBar, QMessageBox
from downloader import list_files, download_files
from systems import get_systems

class DownloaderApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Systèmes
        self.system_label = QLabel('Select a system :')
        layout.addWidget(self.system_label)

        self.system_combo = QComboBox()
        self.system_combo.addItems(get_systems().keys())
        layout.addWidget(self.system_combo)

        # Filtres
        self.filter_label = QLabel('Select a region :')
        layout.addWidget(self.filter_label)

        self.filter_combo = QComboBox()
        self.filter_combo.addItems(["EU", "JP", "US", "WR", "DE", "ES", "FR", "IT"])
        layout.addWidget(self.filter_combo)

        # Bouton de téléchargement
        self.download_button = QPushButton('Download')
        self.download_button.clicked.connect(self.on_download)
        layout.addWidget(self.download_button)

        # Barre de progression
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)

        # Label de progression
        self.progress_label = QLabel('Progress : 0/0')
        layout.addWidget(self.progress_label)

        self.setLayout(layout)
        self.setWindowTitle('Arquivista.exe Downloader')
        self.setGeometry(300, 300, 400, 200)

    def on_download(self):
        # Récupérer le système et le filtre sélectionnés
        selected_system = self.system_combo.currentText()
        selected_filter = self.filter_combo.currentText()
        base_url = get_systems().get(selected_system, None)

        if not base_url:
            QMessageBox.warning(self, "Error", "Please select a system.")
            return

        # Lister les fichiers correspondant au filtre
        files_to_download = list_files(base_url, selected_filter)

        if files_to_download is None or len(files_to_download) == 0:
            QMessageBox.warning(self, "No file found", f"No file including '{selected_filter}' has been found for {selected_system}.")
            return

        # Sélection du dossier de téléchargement
        download_folder = QFileDialog.getExistingDirectory(self, "Downloade")

        if not download_folder:
            QMessageBox.warning(self, "Error", "Please select a folder.")
            return

        # Lancer le téléchargement
        self.download_files(download_folder, files_to_download)

    def download_files(self, download_folder, files_to_download):
        # Callback pour mettre à jour la progression
        def progress_callback(current, total):
            self.progress_bar.setValue(current)
            self.progress_label.setText(f"Progress : {current}/{total}")
            self.progress_bar.setMaximum(total)

        downloaded_count, skipped_count = download_files(download_folder, files_to_download, progress_callback)

        QMessageBox.information(self, "Done", f"Done : {downloaded_count} files downloaded, {skipped_count} skipped.")
