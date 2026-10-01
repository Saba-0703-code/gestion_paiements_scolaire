from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTableWidget,
    QTableWidgetItem, QHeaderView, QMessageBox
)
from data.repositories import EleveRepository, PaiementRepository
from business.services import obtenir_statut_eleve
from ui.paiement_dialog import DialoguePaiement

class EcranFicheEleve(QDialog):
    def __init__(self, id_eleve, parent=None):
        super().__init__(parent)
        self.id_eleve = id_eleve
        self.eleve = EleveRepository.par_id(id_eleve)
        
        if not self.eleve:
            QMessageBox.critical(self, "Erreur", "Élève introuvable")
            self.reject()
            return

        self.setWindowTitle(f"Fiche — {self.eleve['nom']} {self.eleve['prenom']}")
        self.resize(700, 500)
        self.creer_interface()
        self.actualiser()

    def creer_interface(self):
        layout = QVBoxLayout(self)

        # En-tête
        entete = QHBoxLayout()
        infos = QVBoxLayout()
        self.label_nom = QLabel()
        self.label_nom.setStyleSheet("font-size: 16pt; font-weight: bold;")
        self.label_classe = QLabel()
        self.label_statut = QLabel()
        self.label_statut.setStyleSheet("font-weight: bold;")
        infos.addWidget(self.label_nom)
        infos.addWidget(self.label_classe)
        infos.addWidget(self.label_statut)
        entete.addLayout(infos)
        entete.addStretch()

        # Solde
        self.label_solde = QLabel()
        self.label_solde.setStyleSheet("font-size: 14pt;")
        entete.addWidget(self.label_solde)
        layout.addLayout(entete)

        # BOUTON — CONNEXION VÉRIFIÉE
        self.bouton_versement = QPushButton("➕ Enregistrer un versement")
        self.bouton_versement.clicked.connect(self.ajouter_paiement)
        layout.addWidget(self.bouton_versement)

        # Tableau historique
        self.tableau = QTableWidget()
        self.tableau.setColumnCount(4)
        self.tableau.setHorizontalHeaderLabels(["Date", "Montant", "Mode", "N° Reçu"])
        for col in range(4):
            self.tableau.horizontalHeader().setSectionResizeMode(col, QHeaderView.Stretch)
        layout.addWidget(self.tableau)

    def actualiser(self):
        self.eleve = EleveRepository.par_id(self.id_eleve)
        versement_total = EleveRepository.total_verse(self.id_eleve)
        solde_restant = self.eleve["montant_total_du"] - versement_total
        self.label_solde.setText(f"Solde restant : <br>{solde_restant:,.0f} FCFA</b>")
        
        statut = obtenir_statut_eleve(self.id_eleve)

        self.label_nom.setText(f"{self.eleve['nom']} {self.eleve['prenom']}")
        self.label_classe.setText(f"{self.eleve['classe']} — {self.eleve['annee_scolaire']}")
        self.label_statut.setText(f"Statut : {statut}")
        self.label_solde.setText(f"Solde restant : <b>{solde_restant:,} FCFA</b>")

        paiements = PaiementRepository.historique(self.id_eleve)
        self.tableau.setRowCount(0)
        for p in paiements:
            ligne = self.tableau.rowCount()
            self.tableau.insertRow(ligne)
            self.tableau.setItem(ligne, 0, QTableWidgetItem(p["date_paiement"]))
            self.tableau.setItem(ligne, 1, QTableWidgetItem(f"{p['montant_verse']:,} FCFA"))
            self.tableau.setItem(ligne, 2, QTableWidgetItem(p["mode_paiement"]))
            self.tableau.setItem(ligne, 3, QTableWidgetItem(p["numero_recu"]))

    def ajouter_paiement(self):
        dlg = DialoguePaiement(self.id_eleve, self)
        if dlg.exec():
            self.actualiser()