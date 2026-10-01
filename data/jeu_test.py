"""
Jeu de données de test — Application Gestion des Paiements Scolaires
15 élèves répartis sur 3 statuts : Soldé / Partiellement payé / Non payé
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

    # Réinitialiser les tables
    cur.execute("DELETE FROM paiement")
    cur.execute("DELETE FROM eleve")
    cur.execute("DELETE FROM sqlite_sequence WHERE name='eleve' OR name='paiement'")

    # Liste des 15 élèves
    eleves = [
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
    cur.execute("SELECT id_eleve, nom, prenom FROM eleve")
    lignes = cur.fetchall()
    ids = {f"{nom} {prenom}": eid for eid, nom, prenom in lignes}

    # Paiements — mode EXACTEMENT conforme à la contrainte CHECK
    paiements = [
        # === SOLDÉS (solde = 0) ===
        (ids["KOUASSI Ama"],          "2025-10-02",  37500, "espèces",      "REC-2025-0001"),
        (ids["KOUASSI Ama"],          "2025-11-15",  37500, "mobile money", "REC-2025-0002"),
        (ids["SABA Akouété Félicio"], "2025-10-05",  42500, "virement",     "REC-2025-0003"),
        (ids["SABA Akouété Félicio"], "2025-12-01",  42500, "virement",     "REC-2025-0004"),
        (ids["AGBENOU Rachid"],       "2025-10-10", 100000, "chèque",       "REC-2025-0005"),

        # === PARTIELLEMENT PAYÉS ===
        (ids["DOVI Kossi"],           "2025-10-08",  25000, "espèces",      "REC-2025-0006"),
        (ids["N'GUESSAN Bénédicte"],  "2025-10-12",  30000, "mobile money", "REC-2025-0007"),
        (ids["ADJO Komlan"],          "2025-11-03",  45000, "espèces",      "REC-2025-0008"),
        (ids["DOGBE Mawuli"],         "2025-10-20",  47500, "virement",     "REC-2025-0009"),
        (ids["LARE Fataou"],          "2025-11-10",  60000, "mobile money", "REC-2025-0010"),
        (ids["GNASSINGBE Komi"],       "2025-10-25",  65000, "chèque",       "REC-2025-0011"),
    ]

    for p in paiements:
        cur.execute("""
            INSERT INTO paiement (id_eleve, date_paiement, montant_verse, mode_paiement, numero_recu)
            VALUES (?, ?, ?, ?, ?)
        """, p)

    conn.commit()
    conn.close()

    # Décompte
    nb_soldes = 3
    nb_partiels = 6
    nb_non_payes = 6

    print(f"\n✅ {len(eleves)} élèves chargés")
    print(f"✅ {len(paiements)} paiements enregistrés")
    print(f"\n📊 Répartition des paiements :")
    print(f"   - Soldés      : {nb_soldes} élève(s)")
    print(f"   - Partiels    : {nb_partiels} élève(s)")
    print(f"   - Non payés   : {nb_non_payes} élève(s)")
    print(f"\n✨ Jeu de données prêt ! Lancez : python main.py")

if __name__ == "__main__":
    creer_jeu_de_donnees()