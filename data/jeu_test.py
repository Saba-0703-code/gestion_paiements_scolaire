import sys
import os

# Ajouter la racine du projet au chemin
dossier_projet = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if dossier_projet not in sys.path:
    sys.path.insert(0, dossier_projet)

from data.repositories import EleveRepository, PaiementRepository
from data.database import get_connection

def vider_donnees():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM paiement")
    cur.execute("DELETE FROM eleve")
    conn.commit()
    conn.close()
    print("🗑️ Base vidée")

def inserer_jeu_de_donnees():
    eleves = [
        # Soldés
        ("Kouassi", "Jean", "CM2", "2025-2026", 150000),
        ("Amen", "Marie", "CM1", "2025-2026", 140000),
        ("Teko", "Paul", "6ème", "2025-2026", 180000),
        ("Bali", "Anne", "CE2", "2025-2026", 130000),
        ("Doe", "David", "3ème", "2025-2026", 200000),
        
        # Partiellement payés
        ("Mensah", "Sylvain", "5ème", "2025-2026", 180000),
        ("Adjo", "Esther", "CM2", "2025-2026", 150000),
        ("Koffi", "Bernard", "4ème", "2025-2026", 190000),
        ("Zoh", "Fatou", "CE1", "2025-2026", 120000),
        ("Lomo", "Gédéon", "CP2", "2025-2026", 100000),
        
        # Non payés
        ("Sama", "Lucie", "CM1", "2025-2026", 140000),
        ("Tia", "Marc", "6ème", "2025-2026", 180000),
        ("Boko", "Ruth", "CE2", "2025-2026", 130000),
        ("Dedi", "Samuel", "5ème", "2025-2026", 175000),
        ("Zion", "Emma", "CP1", "2025-2026", 95000),
    ]
    
    id_eleves = []
    for nom, prenom, classe, annee, montant in eleves:
        id_e = EleveRepository.ajouter(nom, prenom, classe, annee, montant)
        id_eleves.append(id_e)
    print(f"✅ {len(eleves)} élèves ajoutés")
    
    # Soldés
    PaiementRepository.enregistrer(id_eleves[0], 75000, "espèces", "2025-10-05")
    PaiementRepository.enregistrer(id_eleves[0], 75000, "chèque", "2025-12-10")
    PaiementRepository.enregistrer(id_eleves[1], 140000, "mobile money", "2025-11-15")
    PaiementRepository.enregistrer(id_eleves[2], 90000, "virement", "2025-10-20")
    PaiementRepository.enregistrer(id_eleves[2], 90000, "espèces", "2025-12-05")
    PaiementRepository.enregistrer(id_eleves[3], 65000, "espèces", "2025-10-08")
    PaiementRepository.enregistrer(id_eleves[3], 65000, "mobile money", "2025-11-28")
    PaiementRepository.enregistrer(id_eleves[4], 200000, "chèque", "2025-12-01")
    
    # Partiels
    PaiementRepository.enregistrer(id_eleves[5], 60000, "espèces", "2025-10-12")
    PaiementRepository.enregistrer(id_eleves[6], 50000, "mobile money", "2025-11-03")
    PaiementRepository.enregistrer(id_eleves[7], 95000, "virement", "2025-10-25")
    PaiementRepository.enregistrer(id_eleves[8], 40000, "espèces", "2025-11-10")
    PaiementRepository.enregistrer(id_eleves[9], 30000, "espèces", "2025-10-30")
    
    print("✅ Paiements insérés")
    print("\n Résumé : 5 soldés | 5 partiels | 5 non payés = 15 élèves")

if __name__ == "__main__":
    reponse = input(" Vider la base existante et charger le jeu de test ? (oui/non) : ")
    if reponse.strip().lower() == "oui":
        vider_donnees()
        inserer_jeu_de_donnees()
        print("\n🎉 Jeu de données prêt !")
    else:
        print("❌ Annulé.")