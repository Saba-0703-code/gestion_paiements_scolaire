from PySide6.QtGui import QFont   # ← À ajouter parmi les imports
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox,
    QComboBox, QDialog, QLabel, QSpinBox, QDoubleSpinBox
)
from data.repositories import EleveRepository
from business.services import enregistrer_paiement_securise

class FormulaireEleve(QDialog):
    def __init__(self, parent=None, eleve=None):
        super().__init__(parent)
        self.setWindowTitle("Fiche Élève")
        self.resize(400, 350)
        self.eleve = eleve
        disposition = QVBoxLayout(self)

        # Champs
        self.champ_nom = QLineEdit()
        self.champ_prenom = QLineEdit()
        self.champ_classe = QComboBox()
        self.champ_classe.addItems(["CP1", "CP2", "CE1", "CE2", "CM1", "CM2", "6ème", "5ème", "4ème", "3ème"])
        self.champ_annee = QLineEdit("2025-2026")
        self.champ_montant = QDoubleSpinBox()
        self.champ_montant.setRange(100, 1000000)
        self.champ_montant.setPrefix("FCFA ")

        for etiquette, champ in [
            ("Nom", self.champ_nom),
            ("Prénom", self.champ_prenom),
            ("Classe", self.champ_classe),
            ("Année scolaire", self.champ_annee),
            ("Montant total dû", self.champ_montant)
        ]:
            disposition.addWidget(QLabel(f"<b>{etiquette}</b>"))
            disposition.addWidget(champ)

        # Pré-remplissage si modification
        if eleve:
            self.champ_nom.setText(eleve["nom"])
            self.champ_prenom.setText(eleve["prenom"])
            self.champ_classe.setCurrentText(eleve["classe"])
            self.champ_annee.setText(eleve["annee_scolaire"])
            self.champ_montant.setValue(eleve["montant_total_du"])

        # Boutons
        btns = QHBoxLayout()
        btn_valider = QPushButton("Enregistrer")
        btn_annuler = QPushButton("Annuler")
        btns.addWidget(btn_valider)
        btns.addWidget(btn_annuler)
        disposition.addLayout(btns)

        btn_valider.clicked.connect(self.valider)
        btn_annuler.clicked.connect(self.reject)

    def valider(self):
        nom = self.champ_nom.text().strip()
        prenom = self.champ_prenom.text().strip()
        classe = self.champ_classe.currentText()
        annee = self.champ_annee.text().strip()
        montant = self.champ_montant.value()

        if not nom or not prenom:
            QMessageBox.warning(self, "Erreur", "Nom et prénom sont obligatoires.")
            return

        if self.eleve:
            EleveRepository.modifier(self.eleve["id_eleve"], nom, prenom, classe, annee, montant)
        else:
            EleveRepository.ajouter(nom, prenom, classe, annee, montant)

        self.accept()


class EcranListeEleves(QWidget):
    def __init__(self, fonction_ouvrir_fiche):
        super().__init__()
        self.ouvrir_fiche = fonction_ouvrir_fiche
        disposition = QVBoxLayout(self)
        disposition.setContentsMargins(20, 20, 20, 20)

        # Barre de recherche
        barre = QHBoxLayout()
        self.recherche = QLineEdit()
        self.recherche.setPlaceholderText("Rechercher un élève (nom, prénom)...")
        self.filtre_classe = QComboBox()
        self.filtre_classe.addItem("Toutes les classes")
        self.actualiser_classes()

        btn_ajouter = QPushButton("➕ Nouvel élève")
        barre.addWidget(self.recherche)
        barre.addWidget(self.filtre_classe)
        barre.addWidget(btn_ajouter)
        disposition.addLayout(barre)

        # Tableau
        self.tableau = QTableWidget()
        self.tableau.setColumnCount(6)
        self.tableau.setHorizontalHeaderLabels(["ID", "Nom", "Classe", "Total dû", "Versé", "Statut"])
        self.tableau.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableau.setSelectionBehavior(QTableWidget.SelectRows)
        disposition.addWidget(self.tableau)

        # Actions sur ligne
        self.tableau.cellDoubleClicked.connect(self.voir_fiche)
        btn_ajouter.clicked.connect(self.ajouter_eleve)
        self.recherche.textChanged.connect(self.actualiser_liste)
        self.filtre_classe.currentTextChanged.connect(self.actualiser_liste)

        self.actualiser_liste()

    def actualiser_classes(self):
        self.filtre_classe.clear()
        self.filtre_classe.addItem("Toutes les classes")
        for c in EleveRepository.liste_classes():
            self.filtre_classe.addItem(c)

    def actualiser_liste(self):
        texte = self.recherche.text().strip()
        classe = self.filtre_classe.currentText()
        if classe == "Toutes les classes":
            classe = ""

        eleves = EleveRepository.tous(texte, classe)
        self.tableau.setRowCount(len(eleves))

        for ligne, e in enumerate(eleves):
            self.tableau.setItem(ligne, 0, QTableWidgetItem(str(e["id_eleve"])))
            self.tableau.setItem(ligne, 1, QTableWidgetItem(f"{e['nom']} {e['prenom']}"))
            self.tableau.setItem(ligne, 2, QTableWidgetItem(e["classe"]))
            self.tableau.setItem(ligne, 3, QTableWidgetItem(f"{e['montant_total_du']:,} FCFA"))
            self.tableau.setItem(ligne, 4, QTableWidgetItem(f"{e['total_verse']:,} FCFA"))
            statut_item = QTableWidgetItem(e["statut"])
            if e["statut"] == "Soldé":
                statut_item.setFont(QFont("Segoe UI", QFont.Bold))
            self.tableau.setItem(ligne, 5, statut_item)

        self.tableau.hideColumn(0)  # ID caché

    def ajouter_eleve(self):
        dlg = FormulaireEleve(self)
        if dlg.exec():
            self.actualiser_liste()
            self.actualiser_classes()

    def voir_fiche(self, ligne, colonne):
        id_eleve = int(self.tableau.item(ligne, 0).text())
        self.ouvrir_fiche(id_eleve)

        __all__ = ["EcranFicheEleve"]