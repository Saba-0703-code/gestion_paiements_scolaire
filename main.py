import sys
import os

# Ajouter la racine du projet au chemin de recherche Python
dossier_projet = os.path.dirname(os.path.abspath(__file__))
if dossier_projet not in sys.path:
    sys.path.insert(0, dossier_projet)

print(f"📂 Chemin projet ajouté : {dossier_projet}")
print(f"🔍 Modules détectés : {os.listdir(dossier_projet)}")

from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow

def charger_style():
    chemin = os.path.join(dossier_projet, "resources", "style.qss")
    if os.path.exists(chemin):
        with open(chemin, "r", encoding="utf-8") as f:
            return f.read()
    return ""

if __name__ == "__main__":
    print("🚀 Démarrage...")
    app = QApplication(sys.argv)
    app.setStyleSheet(charger_style())
    
    fenetre = MainWindow()
    fenetre.show()
    print("✅ Fenêtre ouverte !")
    sys.exit(app.exec())