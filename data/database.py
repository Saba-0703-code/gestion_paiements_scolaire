import sqlite3
import os

CHEMIN_BASE = os.path.join(os.path.dirname(__file__), "gestion_paiements.db")

def creer_tables():
    """Crée les tables si elles n'existent pas — schéma conforme aux besoins"""
    conn = sqlite3.connect(CHEMIN_BASE)
    cur = conn.cursor()

    # Table Élève
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

    # Table Paiement
    cur.execute("""
        CREATE TABLE IF NOT EXISTS paiement (
            id_paiement INTEGER PRIMARY KEY AUTOINCREMENT,
            numero_recu TEXT UNIQUE NOT NULL,
            id_eleve INTEGER NOT NULL,
            montant_verse REAL NOT NULL CHECK (montant_verse > 0),
            date_paiement TEXT NOT NULL,
            mode_paiement TEXT NOT NULL CHECK (mode_paiement IN ('espèces', 'chèque', 'virement', 'mobile money')),
            FOREIGN KEY (id_eleve) REFERENCES eleve(id_eleve) ON DELETE RESTRICT
        )
    """)

    # Vue : solde et statut par élève
    cur.execute("""
        CREATE VIEW IF NOT EXISTS vue_solde_eleve AS
        SELECT
            e.id_eleve,
            e.nom,
            e.prenom,
            e.classe,
            e.annee_scolaire,
            e.montant_total_du,
            COALESCE(SUM(p.montant_verse), 0) AS total_verse,
            e.montant_total_du - COALESCE(SUM(p.montant_verse), 0) AS solde_restant,
            CASE
                WHEN e.montant_total_du - COALESCE(SUM(p.montant_verse), 0) = 0 THEN 'Soldé'
                WHEN COALESCE(SUM(p.montant_verse), 0) > 0 THEN 'Partiellement payé'
                ELSE 'Non payé'
            END AS statut
        FROM eleve e
        LEFT JOIN paiement p ON e.id_eleve = p.id_eleve
        GROUP BY e.id_eleve
    """)

    conn.commit()
    conn.close()

def get_connection():
    """Retourne une connexion vers la base"""
    conn = sqlite3.connect(CHEMIN_BASE)
    conn.row_factory = sqlite3.Row
    return conn

# Créer les tables à l'import du module
creer_tables()