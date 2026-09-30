from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox
)
from data.repositories import EleveRepository, PaiementRepository
from ui.paiement_dialog import DialoguePaiement


class EcranFicheEleve(QWidget):
    def __init__(self, id_eleve, fonction_retour):
        super().__init__()
        self.id_eleve = id_eleve
        self.retour = fonction_retour
        disposition = QVBoxLayout(self)
        disposition.setContentsMargins(20, 20, 20, 20)

        # En-tête
        haut = QHBoxLayout()
        self.btn_retour = QPushButton("← Retour")
        haut.addWidget(self.btn_retour)
        haut.addStretch()
        disposition.addLayout(haut)

        # Infos élève
        self.etiquette_nom = QLabel()
        self.etiquette_nom.setStyleSheet("font-size: 18px; font-weight: bold;")
        disposition.addWidget(self.etiquette_nom)

        self.etat_solde = QLabel()
        self.etat_solde.setStyleSheet("font-size: 14px;")
        disposition.addWidget(self.etat_solde)

        # Bouton paiement
        self.btn_payer = QPushButton("➕ Enregistrer un versement")
        disposition.addWidget(self.btn_payer)
        disposition.addSpacing(15)

        # Historique
        disposition.addWidget(QLabel("<b>Historique des paiements</b>"))
        self.historique = QTableWidget()
        self.historique.setColumnCount(5)
        self.historique.setHorizontalHeaderLabels(["Date", "N° Reçu", "Mode", "Montant", "Action"])
        self.historique.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        disposition.addWidget(self.historique)

        # Connexions
        self.btn_retour.clicked.connect(self.retour)
        self.btn_payer.clicked.connect(self.ouvrir_dialogue_paiement)

        self.actualiser()

    def actualiser(self):
        e = EleveRepository.par_id(self.id_eleve)
        if not e:
            return

        self.etiquette_nom.setText(f"{e['nom']} {e['prenom']} — {e['classe']} ({e['annee_scolaire']})")
        self.etat_solde.setText(
            f"Total dû : {e['montant_total_du']:,} FCFA  |  "
            f"Versé : {e['total_verse']:,} FCFA  |  "
            f"Solde restant : {e['solde_restant']:,} FCFA  |  "
            f"<b>{e['statut']}</b>"
        )

        # Historique
        paiements = PaiementRepository.historique(self.id_eleve)
        self.historique.setRowCount(len(paiements))
        for ligne, p in enumerate(paiements):
            self.historique.setItem(ligne, 0, QTableWidgetItem(p["date_paiement"]))
            self.historique.setItem(ligne, 1, QTableWidgetItem(p["numero_recu"]))
            self.historique.setItem(ligne, 2, QTableWidgetItem(p["mode_paiement"]))
            self.historique.setItem(ligne, 3, QTableWidgetItem(f"{p['montant_verse']:,} FCFA"))
            btn_voir = QPushButton("Voir reçu")
            btn_voir.clicked.connect(lambda _, n=p["numero_recu"]: self.voir_recu(n))
            self.historique.setCellWidget(ligne, 4, btn_voir)

    def ouvrir_dialogue_paiement(self):
        e = EleveRepository.par_id(self.id_eleve)
        dlg = DialoguePaiement(self, self.id_eleve, f"{e['nom']} {e['prenom']}", e["solde_restant"])
        if dlg.exec():
            self.actualiser()

    def voir_recu(self, numero):
        from business.services import creer_recu_pdf, ouvrir_pdf
        succes, message, chemin = creer_recu_pdf(numero)
        if succes:
            QMessageBox.information(self, "Reçu", message)
            ouvrir_pdf(chemin)
        else:
            QMessageBox.warning(self, "Erreur", message)