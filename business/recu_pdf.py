import os
from fpdf import FPDF

DOSSIER_RECUS = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "recus"
)
os.makedirs(DOSSIER_RECUS, exist_ok=True)

class RecuPDF(FPDF):
    def header(self):
        # Bandeau bleu
        self.set_fill_color(21, 101, 192)
        self.rect(0, 0, 210, 35, "F")
        
        # Titre en blanc
        self.set_font("Helvetica", "B", 22)
        self.set_text_color(255, 255, 255)
        self.set_xy(0, 10)
        self.cell(0, 12, "RECU DE PAIEMENT SCOLAIRE", ln=True, align="C")
        
        # Sous-titre avec tiret SIMPLE
        self.set_font("Helvetica", "", 11)
        self.set_xy(0, 24)
        self.cell(0, 8, "EduPaie - Gestion des Paiements Scolaires", ln=True, align="C")
        
        self.ln(8)
        self.set_text_color(0, 0, 0)

    def footer(self):
        self.set_y(-20)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(120, 120, 120)
        self.cell(0, 6, "Document genere automatiquement", align="C")
        self.ln(5)
        self.cell(0, 6, "Page " + str(self.page_no()), align="C")

def generer_recu_pdf(eleve, paiement, solde_apres):
    pdf = RecuPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Numero de recu
    pdf.set_font("Helvetica", "B", 14)
    pdf.set_fill_color(230, 240, 255)
    pdf.cell(130)
    pdf.cell(60, 12, f"N° {paiement['numero_recu']}", border=1, fill=True, align="C")
    pdf.ln(20)

    # Infos eleve
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 10, "INFORMATIONS DE L'ELEVE", ln=True)
    pdf.set_font("Helvetica", "", 11)
    
    pdf.set_draw_color(200, 200, 200)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)

    pdf.cell(55, 8, "Nom et prenom :")
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(0, 8, f"{eleve['nom']} {eleve['prenom']}", ln=True)
    pdf.set_font("Helvetica", "", 11)

    pdf.cell(55, 8, "Classe / Niveau :")
    pdf.cell(0, 8, f"{eleve['classe']}  -  Annee : {eleve['annee_scolaire']}", ln=True)

    pdf.cell(55, 8, "Date du versement :")
    pdf.cell(0, 8, paiement["date_paiement"], ln=True)
    pdf.ln(8)

    # Detail du paiement
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 10, "DETAIL DU VERSEMENT", ln=True)
    pdf.set_font("Helvetica", "", 11)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)

    pdf.set_fill_color(245, 245, 245)
    pdf.cell(80, 10, "Mode de paiement", border=1, fill=True)
    pdf.cell(100, 10, "Montant verse", border=1, fill=True, ln=True)
    
    pdf.cell(80, 10, paiement["mode_paiement"], border=1)
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(100, 10, f"{paiement['montant_verse']:,.0f} FCFA", border=1, ln=True)
    pdf.ln(10)

    # Solde restant
    pdf.set_font("Helvetica", "B", 13)
    pdf.set_fill_color(255, 245, 204)
    pdf.cell(130, 12, "SOLDE RESTANT DU", border=1, fill=True)
    pdf.set_text_color(153, 102, 0)
    pdf.cell(60, 12, f"{solde_apres:,.0f} FCFA", border=1, fill=True, align="C", ln=True)
    pdf.set_text_color(0, 0, 0)
    pdf.ln(15)

    # Signatures
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(90, 8, "Signature du responsable financier :", ln=False)
    pdf.cell(90, 8, "Signature du parent / responsable legal :", ln=True)
    pdf.ln(25)

    # Enregistrer
    chemin_fichier = os.path.join(DOSSIER_RECUS, f"{paiement['numero_recu']}.pdf")
    pdf.output(chemin_fichier)
    return chemin_fichier