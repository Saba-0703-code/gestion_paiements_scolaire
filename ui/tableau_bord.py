from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PySide6.QtCore import Qt
from business.services import obtenir_donnees_tableau_de_bord


class EcranTableauBord(QWidget):
    def __init__(self):
        super().__init__()
        disposition = QVBoxLayout(self)
        disposition.setContentsMargins(30, 30, 30, 30)

        titre = QLabel(" Tableau de bord")
        titre.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 20px;")
        disposition.addWidget(titre)

        # Cartes indicateurs
        cartes = QHBoxLayout()
        self.carte_eleves = self.creer_carte("Élèves inscrits", "0")
        self.carte_encaisse = self.creer_carte("Total encaissé", "0 FCFA")
        self.carte_du = self.creer_carte("Total restant dû", "0 FCFA")
        self.carte_non_soldes = self.creer_carte("Élèves non soldés", "0")

        for c in [self.carte_eleves, self.carte_encaisse, self.carte_du, self.carte_non_soldes]:
            cartes.addWidget(c)
        disposition.addLayout(cartes)
        disposition.addStretch()

        self.actualiser()

    def creer_carte(self, etiquette, valeur):
        cadre = QWidget()
        cadre.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 8px;
                padding: 20px;
                border: 1px solid #E0E0E0;
            }
        """)
        disp = QVBoxLayout(cadre)
        lbl_val = QLabel(valeur)
        lbl_val.setStyleSheet("font-size: 22px; font-weight: bold; color: #1565C0;")
        lbl_etiquette = QLabel(etiquette)
        lbl_etiquette.setStyleSheet("color: #607D8B;")
        disp.addWidget(lbl_val, alignment=Qt.AlignCenter)
        disp.addWidget(lbl_etiquette, alignment=Qt.AlignCenter)
        return cadre

    def actualiser(self):
        d = obtenir_donnees_tableau_de_bord()
        self.carte_eleves.findChild(QLabel, "", Qt.FindDirectChildrenOnly).setText(str(d["nb_eleves"]))
        self.carte_encaisse.findChildren(QLabel)[0].setText(f"{d['total_verse']:,} FCFA")
        self.carte_du.findChildren(QLabel)[0].setText(f"{d['total_restant']:,} FCFA")
        self.carte_non_soldes.findChildren(QLabel)[0].setText(str(d["nb_non_soldes"]))