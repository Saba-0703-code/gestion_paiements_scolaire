from fpdf import FPDF
import os
from datetime import datetime

class GenerateurRecuPDF(FPDF):
    """Génère un reçu au format PDF — charte graphique : BLEU + BLANC uniquement"""

    def en_tete(self):
        """En-tête du reçu — conforme à la charte"""
        # Bandeau bleu
        self.set_fill_color(21, 101, 192)  # #1565C0
        self.set_text_color(255, 255, 255)  # Blanc
        self.set_font("Helvetica", "B", 16)
        self.cell(0, 15, "REÇU DE PAIEMENT SCOLAIRE", fill=True, align="C")
        self.ln(12)
        self.set_text_color(38, 50, 56)  # Texte sombre
        self.set_font("Helvetica", "", 10)
        self.cell(0, 6, "Établissement : Gestion des Paiements Scolaires", align="C")
        self.ln(8)

    def corps(self, numero_recu, nom_eleve, classe, annee, montant, mode, date, total_verse, solde_restant):
        """Corps du reçu — toutes les infos obligatoires"""
        self.set_font("Helvetica", "", 11)
        
        # Numéro unique
        self.set_font("Helvetica", "B", 11)
        self.cell(0, 8, f"N° Reçu : {numero_recu}")
        self.ln(10)
        
        # Infos élève
        self.set_font("Helvetica", "", 11)
        self.cell(60, 8, "Élève :")
        self.set_font("Helvetica", "B", 11)
        self.cell(0, 8, nom_eleve)
        self.ln(7)
        
        self.set_font("Helvetica", "", 11)
        self.cell(60, 8, "Classe :")
        self.cell(0, 8, f"{classe}  |  Année scolaire : {annee}")
        self.ln(12)
        
        # Ligne séparateur
        self.set_draw_color(21, 101, 192)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(8)
        
        # Détail du versement
        self.set_font("Helvetica", "B", 12)
        self.cell(0, 10, "VERSEMENT EFFECTUÉ", align="C")
        self.ln(10)
        
        self.set_font("Helvetica", "", 11)
        self.cell(60, 8, "Date :")
        self.cell(0, 8, date)
        self.ln(7)
        
        self.cell(60, 8, "Mode de paiement :")
        self.cell(0, 8, mode.capitalize())
        self.ln(7)
        
        self.set_font("Helvetica", "B", 14)
        self.cell(60, 12, "MONTANT VERSÉ :")
        self.cell(0, 12, f"{montant:,.0f} FCFA")
        self.ln(15)
        
        # Résumé du compte
        self.set_font("Helvetica", "B", 11)
        self.cell(0, 8, "Résumé du compte", border="B")
        self.ln(10)
        
        self.set_font("Helvetica", "", 11)
        self.cell(60, 8, "Total déjà versé :")
        self.cell(0, 8, f"{total_verse:,.0f} FCFA")
        self.ln(7)
        
        self.cell(60, 8, "Solde restant dû :")
        self.set_text_color(21, 101, 192)
        self.cell(0, 8, f"{solde_restant:,.0f} FCFA")
        self.set_text_color(38, 50, 56)
        self.ln(20)
        
        # Signature
        self.cell(100)
        self.cell(0, 8, "Signature : _________________________")
        self.ln(15)
        
        # Pied de page
        self.set_font("Helvetica", "", 8)
        self.set_text_color(96, 125, 139)
        self.cell(0, 6, f"Document généré le {datetime.now().strftime('%Y-%m-%d à %H:%M:%S')}", align="C")
        self.ln(5)
        self.cell(0, 6, "Reçu numéroté — unique et invariable", align="C")

def generer_recu_pdf(donnees_recu, dossier_sortie="recus"):
    """
    Génère le PDF et retourne le chemin du fichier
    donnees_recu = dictionnaire contenant :
        numero_recu, nom_eleve, classe, annee,
        montant, mode, date, total_verse, solde_restant
    """
    # Créer le dossier de stockage si besoin
    if not os.path.exists(dossier_sortie):
        os.makedirs(dossier_sortie)
    
    chemin_fichier = os.path.join(dossier_sortie, f"{donnees_recu['numero_recu']}.pdf")
    
    # Génération
    pdf = GenerateurRecuPDF(orientation="P", unit="mm", format="A4")
    pdf.add_page()
    pdf.en_tete()
    pdf.corps(
        numero_recu=donnees_recu["numero_recu"],
        nom_eleve=donnees_recu["nom_eleve"],
        classe=donnees_recu["classe"],
        annee=donnees_recu["annee"],
        montant=donnees_recu["montant"],
        mode=donnees_recu["mode"],
        date=donnees_recu["date"],
        total_verse=donnees_recu["total_verse"],
        solde_restant=donnees_recu["solde_restant"]
    )
    
    pdf.output(chemin_fichier)
    return chemin_fichier