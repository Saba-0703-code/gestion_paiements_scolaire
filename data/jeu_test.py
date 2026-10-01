"""
Jeu de données de test — Application Gestion Paiements Scolaires
15 élèves répartis sur plusieurs statuts : Soldé / Partiellement payé / Non payé
"""

import sqlite3
import os

CHEMIN_DB = os.path.join(os.path.dirname(__file__), "gestion_paiements.db")

def creer_jeu_de_donnees():
    reponse = input("Créer le jeu de données de test (écrase les données existantes) ? [oui/non] : ").strip().lower()
    if reponse != "oui":
        print("❌ Annulé.")
        return

    conn = sqlite3.connect(CHEMIN_DB)
    cur = conn.cursor()

    # Réinitialiser
    cur.execute("DELETE FROM paiement")
    cur.execute("DELETE FROM eleve")

    eleves = [
        # (nom, prenom, classe, annee, montant_total)
        ("KOUASSI", "Ama", "CP1", "2025-2026", 75000),
        ("DOVI", "Kossi", "CP1", "2025-2026", 75000),
        ("SABA", "Akouété Félicio", "CE1", "2025-2026", 85000),
        ("N'GUESSAN", "Bénédicte", "CE1", "2025-2026", 85000),
        ("ADJO", "Komlan", "CE2", "2025-2026", 90000),
        ("AKPOVI", "Sylvie", "CE2", "2025-2026", 90000),
        ("DOGBE", "Mawuli", "CM1", "2025-2026", 95000),
        ("SEGBE", "Essossinam", "CM1", "2025-2026", 95000),
        ("AGBENOU", "Rachid", "CM2", "2025-2026", 100000),
        ("KPELI", "Reine", "CM2", "2025-2026", 100000),
        ("LARE", "Fataou", "6ème", "2025-2026", 120000),
        ("TCHAO", "Julienne", "6ème", "2025-2026", 120000),
        ("GNASSINGBE", "Komi", "5ème", "2025-2026", 130000),
        ("AKAKPO", "Dédé", "5ème", "2025-2026", 130000),
        ("HOUNKPATIN", "Espoir", "4ème", "2025-2026", 145000),
    ]

    for e in eleves:
        cur.execute("""
            INSERT INTO eleve (nom, prenom, classe, annee_scolaire, montant_total_du)
            VALUES (?, ?, ?, ?, ?)
        """, e)

    # Récupérer les IDs
    cur.execute("SELECT id_eleve, nom, prenom, classe, montant_total_du FROM eleve")
    liste = cur.fetchall()
    ids = {f"{e[1]} {e[2]}": e[0] for e in liste}

    # Paiements variés
    paiements = [
        # Soldés
        (ids["KOUASSI Ama"], "2025-10-02", 37500, "espèces", "REC-2025-0001"),
        (ids["KOUASSI Ama"], "2025-11-15", 37500, "mobile_money", "REC-2025-0002"),
        (ids["SABA Akouété Félicio"], "2025-10-05", 42500, "virement", "REC-2025-0003"),
        (ids["SABA Ornella victorine"], "2025-12-01", 42500, "virement", "REC-2025-0004"),
        (ids["KPOTI Komlan Eliabe"], "2025-10-10", 100000, "chèque", "REC-2025-0005"),

        # Partiellement payés
        (ids["DOVI Kossi"], "2025-10-08", 25000, "espèces", "REC-2025-0006"),
        (ids["N'GUESSAN Bénédicte"], "2025-10-12", 30000, "mobile_money", "REC-2025-0007"),
        (ids["ADJO Komlan"], "2025-11-03", 45000, "espèces", "REC-2025-0008"),
        (ids["DOGBE Mawuli"], "2025-10-20", 47500, "virement", "REC-2025-0009"),
        (ids["LARE Fataou"], "2025-11-10", 60000, "mobile_money", "REC-2025-0010"),
        (ids["GNASSINGBE Komi"], "2025-10-25", 65000, "chèque", "REC-2025-0011"),

        # Non payés → aucun versement
    ]

    for p in paiements:
        cur.execute("""
            INSERT INTO paiement (id_eleve, date_paiement, montant_verse, mode_paiement, numero_recu)
            VALUES (?, ?, ?, ?, ?)
        """, p)

    conn.commit()
    conn.close()

    print(f"✅ {len(eleves)} élèves chargés")
    print(f"✅ {len(paiements)} paiements enregistrés")
    print("📊 Répartition :")
    print("   - Soldés     : 3 élèves")
    print("   - Partiels   : 6 élèves")
    print("   - Non payés  : 6 élèves")
    print("\n✨ Jeu de données prêt !")

if __name__ == "__main__":
    creer_jeu_de_donnees()