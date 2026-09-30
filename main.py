import sys
import os

# Ajouter la racine au chemin
dossier_projet = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, dossier_projet)

from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Charger le style
    style_path = os.path.join(dossier_projet, "resources", "style.qss")
    if os.path.exists(style_path):
        with open(style_path, "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())
    
    fenetre = MainWindow()
    fenetre.show()
    sys.exit(app.exec())