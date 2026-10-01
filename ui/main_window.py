from PySide6.QtGui import QPixmap
from ui.eleve_form import EcranListeEleves
from ui.tableau_bord import EcranTableauBord

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QStackedWidget, QLabel, QFrame
)
from PySide6.QtCore import Qt
from ui.eleve_form import EcranListeEleves
from ui.tableau_bord import EcranTableauBord
from ui.fiche_eleve import EcranFicheEleve


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestion des Paiements Scolaires")
        self.resize(1000, 650)

        # Widget central
        corps = QWidget()
        self.setCentralWidget(corps)
        disposition = QHBoxLayout(corps)
        disposition.setContentsMargins(0, 0, 0, 0)
        disposition.setSpacing(0)

        # --- Barre latérale ---
        barre_laterale = QFrame()
        barre_laterale.setFixedWidth(200)
        barre_laterale.setStyleSheet("background-color: #0D47A1;")
        disposition_barre = QVBoxLayout(barre_laterale)
        disposition_barre.setContentsMargins(15, 30, 15, 30)
        disposition_barre.setSpacing(10)

        # Titre dans la barre
        titre = QLabel("EduPaie")
        titre.setStyleSheet("color: white; font-size: 15px; font-weight: bold;")
        titre.setAlignment(Qt.AlignCenter)
        disposition_barre.addWidget(titre)
        disposition_barre.addSpacing(20)

        # Boutons de navigation
        self.btn_tableau = QPushButton("Tableau de bord")
        self.btn_eleves = QPushButton("Liste des élèves")
        self.btn_quitter = QPushButton("Quitter")

        for btn in [self.btn_tableau, self.btn_eleves, self.btn_quitter]:
            btn.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    color: white;
                    border: none;
                    text-align: left;
                    padding: 10px;
                    font-size: 14px;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background-color: #1565C0;
                }
            """)

        disposition_barre.addWidget(self.btn_tableau)
        disposition_barre.addWidget(self.btn_eleves)
        disposition_barre.addStretch()
        disposition_barre.addWidget(self.btn_quitter)

        # --- Zone de contenu ---
        self.contenu = QStackedWidget()

        # Écrans
        self.ecran_tableau = EcranTableauBord()
        # Dans __init__ de MainWindow :
        self.ecran_eleves = EcranListeEleves(
             self.afficher_fiche_eleve,
             parent=self
        )
        

        self.contenu.addWidget(self.ecran_tableau)   # index 0
        self.contenu.addWidget(self.ecran_eleves)     # index 1

        # Assemblage
        disposition.addWidget(barre_laterale)
        disposition.addWidget(self.contenu)

        # Connexions
        self.btn_tableau.clicked.connect(lambda: self.contenu.setCurrentIndex(0))
        self.btn_eleves.clicked.connect(lambda: self.contenu.setCurrentIndex(1))
        self.btn_quitter.clicked.connect(self.close)

    def ouvrir_fiche_eleve(self, id_eleve):
        """Ouvre la fiche détaillée d'un élève"""
        from ui.fiche_eleve import EcranFicheEleve
        self.ecran_fiche = EcranFicheEleve(id_eleve, self.retour_liste)
        self.contenu.addWidget(self.ecran_fiche)
        self.contenu.setCurrentWidget(self.ecran_fiche)

    def retour_liste(self):
        """Retourne à la liste des élèves"""
        self.contenu.setCurrentIndex(1)
        if self.ecran_fiche:
            self.contenu.removeWidget(self.ecran_fiche)
            self.ecran_fiche = None

    def afficher_fiche_eleve(self, id_eleve):
        """Ouvre la fiche détaillée d'un élève"""
        from ui.fiche_eleve import EcranFicheEleve
        fiche = EcranFicheEleve(id_eleve, parent=self)
        fiche.exec()        