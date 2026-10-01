import sqlite3
import os

# Chemin vers la base de données
DOSSIER_DATA = os.path.dirname(os.path.abspath(__file__))
CHEMIN_DB = os.path.join(DOSSIER_DATA, "gestion_paiements.db")

def creer_tables():
    """Créer les tables si elles n'existent pas déjà"""
    conn = sqlite3.connect(CHEMIN_DB)
    cur = conn.cursor()

    # Table élève
    cur.execute("""
        CREATE TABLE IF NOT EXISTS eleve (
            id_eleve INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            prenom TEXT NOT NULL,
            classe TEXT NOT NULL,
            annee_scolaire TEXT NOT NULL,
            montant_total_du REAL NOT NULL CHECK (montant_total_du > 0)
        )
    """)

    # Table paiement
    cur.execute("""
        CREATE TABLE IF NOT EXISTS paiement (
            id_paiement INTEGER PRIMARY KEY AUTOINCREMENT,
            id_eleve INTEGER NOT NULL,
            date_paiement TEXT NOT NULL,
            montant_verse REAL NOT NULL CHECK (montant_verse > 0),
            mode_paiement TEXT NOT NULL CHECK (
                mode_paiement IN ('espèces', 'chèque', 'virement', 'mobile money')
            ),
            numero_recu TEXT UNIQUE NOT NULL,
            FOREIGN KEY (id_eleve) REFERENCES eleve(id_eleve) ON DELETE CASCADE
        )
    """)

    conn.commit()
    conn.close()
    print(f"✅ Base de données prête : {CHEMIN_DB}")

# Initialisation automatique à l'import
creer_tables()