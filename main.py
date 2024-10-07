from PyQt5.QtWidgets import QApplication
import sys
from ui import DownloaderApp

def main():
    app = QApplication(sys.argv)
    window = DownloaderApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
