from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLineEdit, QDoubleSpinBox,
    QComboBox, QDateEdit, QDialogButtonBox, QMessageBox, QLabel
)
from PySide6.QtCore import QDate
from business.services import enregistrer_paiement_securise
from data.repositories import EleveRepository

class DialoguePaiement(QDialog):
    def __init__(self, id_eleve, parent=None):
        super().__init__(parent)
        self.id_eleve = id_eleve
        self.setWindowTitle("Enregistrer un versement")
        self.resize(400, 300)

        self.eleve = EleveRepository.par_id(id_eleve)
        if not self.eleve:
            QMessageBox.critical(self, "Erreur", "Élève introuvable")
            self.reject()
            return

        self.creer_interface()

    def creer_interface(self):
        layout = QVBoxLayout(self)

        # Infos élève
        infos = QLabel(f"<b>{self.eleve['nom']} {self.eleve['prenom']}</b> — {self.eleve['classe']}")
        layout.addWidget(infos)

        # Solde actuel
        versement_total = EleveRepository.total_verse(self.id_eleve)
        self.solde_restant = self.eleve["montant_total_du"] - versement_total
        self.label_solde = QLabel(f"Solde restant : <b>{self.solde_restant:,.0f} FCFA</b>")

        # Formulaire
        form = QFormLayout()

        self.montant_edit = QDoubleSpinBox()
        self.montant_edit.setRange(1.0, float(self.solde_restant))
        self.montant_edit.setDecimals(0)
        self.montant_edit.setSuffix(" FCFA")

        self.date_edit = QDateEdit(QDate.currentDate())
        self.date_edit.setDisplayFormat("yyyy-MM-dd")

        self.mode_edit = QComboBox()
        self.mode_edit.addItems(["espèces", "chèque", "virement", "mobile money"])

        form.addRow("Montant versé :", self.montant_edit)
        form.addRow("Date du paiement :", self.date_edit)
        form.addRow("Mode de paiement :", self.mode_edit)

        layout.addLayout(form)

        # Boutons
        boutons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        boutons.accepted.connect(self.valider)
        boutons.rejected.connect(self.reject)
        layout.addWidget(boutons)

    def valider(self):
        montant = self.montant_edit.value()
        date = self.date_edit.date().toString("yyyy-MM-dd")
        mode = self.mode_edit.currentText()

        succes, message, numero_recu, chemin_pdf = enregistrer_paiement_securise(
            self.id_eleve, montant, mode, date
        )

        if succes:
            QMessageBox.information(self, "Succès", f"{message}\nReçu N° {numero_recu}")
            # Ouvrir le PDF
            import os
            import sys
            if chemin_pdf and os.path.exists(chemin_pdf):
                try:
                    if sys.platform == "win32":
                        os.startfile(chemin_pdf)
                except Exception:
                    pass
            self.accept()
        else:
            QMessageBox.warning(self, "Erreur", message)