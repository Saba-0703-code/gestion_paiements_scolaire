from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QGridLayout
from PySide6.QtCore import Qt
from business.services import obtenir_donnees_tableau_de_bord

class EcranTableauBord(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.creer_interface()
        self.actualiser()

    def creer_interface(self):
        layout = QVBoxLayout(self)

        titre = QLabel("📊 Tableau de bord")
        titre.setStyleSheet("font-size: 18pt; font-weight: bold; padding: 10px;")
        titre.setAlignment(Qt.AlignCenter)
        layout.addWidget(titre)

        # Grille des indicateurs
        grille = QGridLayout()
        grille.setSpacing(20)
        grille.setContentsMargins(30, 30, 30, 30)

        self.label_eleves = self._creer_indicateur("Nombre d'élèves", "0")
        self.label_total_du = self._creer_indicateur("Total attendu", "0 FCFA")
        self.label_total_verse = self._creer_indicateur("Total encaissé", "0 FCFA")
        self.label_restant = self._creer_indicateur("Total restant dû", "0 FCFA")
        self.label_non_soldes = self._creer_indicateur("Élèves non soldés", "0")

        grille.addWidget(self.label_eleves, 0, 0)
        grille.addWidget(self.label_total_du, 0, 1)
        grille.addWidget(self.label_total_verse, 1, 0)
        grille.addWidget(self.label_restant, 1, 1)
        grille.addWidget(self.label_non_soldes, 2, 0, 1, 2)

        layout.addLayout(grille)
        layout.addStretch()

    def _creer_indicateur(self, etiquette, valeur):
        cadre = QWidget()
        cadre.setStyleSheet("""
            QWidget {
                background: white;
                border-radius: 8px;
                padding: 20px;
            }
        """)
        boite = QVBoxLayout(cadre)
        lbl_etiquette = QLabel(etiquette)
        lbl_etiquette.setStyleSheet("color: #666; font-size: 11pt;")
        lbl_valeur = QLabel(valeur)
        lbl_valeur.setStyleSheet("font-size: 16pt; font-weight: bold; color: #1565C0;")
        boite.addWidget(lbl_etiquette)
        boite.addWidget(lbl_valeur)
        cadre.label_valeur = lbl_valeur
        return cadre

    def actualiser(self):
        donnees = obtenir_donnees_tableau_de_bord()
        self.label_eleves.label_valeur.setText(str(donnees["nb_eleves"]))
        self.label_total_du.label_valeur.setText(f"{donnees['total_du']:,} FCFA")
        self.label_total_verse.label_valeur.setText(f"{donnees['total_verse']:,} FCFA")
        self.label_restant.label_valeur.setText(f"{donnees['total_restant']:,} FCFA")
        self.label_non_soldes.label_valeur.setText(str(donnees["nb_non_soldes"]))