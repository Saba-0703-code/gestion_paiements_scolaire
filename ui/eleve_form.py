from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QLineEdit, QComboBox, QHeaderView, QDialog, QFormLayout,
    QDialogButtonBox, QMessageBox
)
from data.repositories import EleveRepository
from business.services import obtenir_statut_eleve

# ✅ LA CLASSE DOIT ÊTRE DÉFINIE EN PREMIER DANS LE FICHIER
class FormulaireEleve(QDialog):
    def __init__(self, parent=None, eleve=None):
        super().__init__(parent)
        self.setWindowTitle("Élève")
        self.resize(400, 300)
        self.eleve = eleve

        layout = QFormLayout(self)
        self.nom_edit = QLineEdit()
        self.prenom_edit = QLineEdit()
        self.classe_edit = QLineEdit()
        self.annee_edit = QLineEdit()
        self.montant_edit = QLineEdit()

        layout.addRow("Nom :", self.nom_edit)
        layout.addRow("Prénom :", self.prenom_edit)
        layout.addRow("Classe :", self.classe_edit)
        layout.addRow("Année scolaire :", self.annee_edit)
        layout.addRow("Montant total dû :", self.montant_edit)

        boutons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        boutons.accepted.connect(self.valider)
        boutons.rejected.connect(self.reject)
        layout.addRow(boutons)

        if eleve:
            self.nom_edit.setText(eleve["nom"])
            self.prenom_edit.setText(eleve["prenom"])
            self.classe_edit.setText(eleve["classe"])
            self.annee_edit.setText(eleve["annee_scolaire"])
            self.montant_edit.setText(str(eleve["montant_total_du"]))

    def valider(self):
        try:
            donnees = {
                "nom": self.nom_edit.text().strip(),
                "prenom": self.prenom_edit.text().strip(),
                "classe": self.classe_edit.text().strip(),
                "annee_scolaire": self.annee_edit.text().strip(),
                "montant_total_du": float(self.montant_edit.text().strip())
            }
            if not all(donnees.values()):
                QMessageBox.warning(self, "Erreur", "Tous les champs sont obligatoires")
                return
            if donnees["montant_total_du"] <= 0:
                QMessageBox.warning(self, "Erreur", "Le montant doit être positif")
                return
            self.donnees = donnees
            self.accept()
        except ValueError:
            QMessageBox.warning(self, "Erreur", "Montant invalide")


class EcranListeEleves(QWidget):
    def __init__(self, callback_ouvrir_fiche, parent=None):
        super().__init__(parent)
        self.callback_ouvrir_fiche = callback_ouvrir_fiche
        self.creer_interface()
        self.actualiser_liste()

    def creer_interface(self):
        layout = QVBoxLayout(self)

        barre = QHBoxLayout()
        self.recherche_edit = QLineEdit()
        self.recherche_edit.setPlaceholderText("Rechercher un élève...")
        self.recherche_edit.textChanged.connect(self.actualiser_liste)

        self.filtre_classe = QComboBox()
        self.filtre_classe.addItem("Toutes les classes")
        self.filtre_classe.currentTextChanged.connect(self.actualiser_liste)

        bouton_nouveau = QPushButton("➕ Nouvel élève")
        bouton_nouveau.clicked.connect(self.ajouter_eleve)  # ✅ Connexion présente

        barre.addWidget(self.recherche_edit)
        barre.addWidget(self.filtre_classe)
        barre.addWidget(bouton_nouveau)
        layout.addLayout(barre)

        self.tableau = QTableWidget()
        self.tableau.setColumnCount(6)
        self.tableau.setHorizontalHeaderLabels(["Nom", "Prénom", "Classe", "Total dû", "Versé", "Statut"])
        for col in range(6):
            self.tableau.horizontalHeader().setSectionResizeMode(col, QHeaderView.Stretch)
        self.tableau.doubleClicked.connect(self.ouvrir_fiche)
        layout.addWidget(self.tableau)

        actions = QHBoxLayout()
        self.bouton_modifier = QPushButton("✏️ Modifier")
        self.bouton_modifier.clicked.connect(self.modifier_eleve)
        self.bouton_supprimer = QPushButton("🗑️ Supprimer")
        self.bouton_supprimer.clicked.connect(self.supprimer_eleve)
        actions.addWidget(self.bouton_modifier)
        actions.addWidget(self.bouton_supprimer)
        layout.addLayout(actions)

    def actualiser_liste(self):
        recherche = self.recherche_edit.text().strip().lower()
        classe_filtre = self.filtre_classe.currentText()
        if classe_filtre == "Toutes les classes":
            classe_filtre = None

        eleves = EleveRepository.liste_complete()
        classes = sorted(set(e["classe"] for e in eleves))
        self.filtre_classe.blockSignals(True)
        self.filtre_classe.clear()
        self.filtre_classe.addItem("Toutes les classes")
        self.filtre_classe.addItems(classes)
        if classe_filtre:
            idx = self.filtre_classe.findText(classe_filtre)
            if idx >= 0:
                self.filtre_classe.setCurrentIndex(idx)
        self.filtre_classe.blockSignals(False)

        self.tableau.setRowCount(0)
        for e in eleves:
            nom_complet = f"{e['nom']} {e['prenom']}".lower()
            if recherche and recherche not in nom_complet:
                continue
            if classe_filtre and e["classe"] != classe_filtre:
                continue

            versement_total = EleveRepository.total_verse(e["id_eleve"])
            statut = obtenir_statut_eleve(e["id_eleve"])

            ligne = self.tableau.rowCount()
            self.tableau.insertRow(ligne)
            self.tableau.setItem(ligne, 0, QTableWidgetItem(e["nom"]))
            self.tableau.setItem(ligne, 1, QTableWidgetItem(e["prenom"]))
            self.tableau.setItem(ligne, 2, QTableWidgetItem(e["classe"]))
            self.tableau.setItem(ligne, 3, QTableWidgetItem(f"{e['montant_total_du']:,} FCFA"))
            self.tableau.setItem(ligne, 4, QTableWidgetItem(f"{versement_total:,} FCFA"))
            self.tableau.setItem(ligne, 5, QTableWidgetItem(statut))
            self.tableau.item(ligne, 0).setData(1000, e["id_eleve"])

    def ajouter_eleve(self):
        form = FormulaireEleve(self)  # ✅ La classe est maintenant définie avant son utilisation
        if form.exec() == QDialog.Accepted:
            EleveRepository.ajouter(**form.donnees)
            self.actualiser_liste()

    def modifier_eleve(self):
        ligne = self.tableau.currentRow()
        if ligne < 0:
            return
        id_eleve = self.tableau.item(ligne, 0).data(1000)
        eleve = EleveRepository.par_id(id_eleve)
        form = FormulaireEleve(self, eleve)
        if form.exec() == QDialog.Accepted:
            EleveRepository.modifier(id_eleve, **form.donnees)
            self.actualiser_liste()

    def supprimer_eleve(self):
        ligne = self.tableau.currentRow()
        if ligne < 0:
            return
        id_eleve = self.tableau.item(ligne, 0).data(1000)
        if QMessageBox.question(self, "Confirmer", "Supprimer cet élève ?") == QMessageBox.Yes:
            EleveRepository.supprimer(id_eleve)
            self.actualiser_liste()

    def ouvrir_fiche(self, index):
        id_eleve = self.tableau.item(index.row(), 0).data(1000)
        if self.callback_ouvrir_fiche:
            self.callback_ouvrir_fiche(id_eleve)