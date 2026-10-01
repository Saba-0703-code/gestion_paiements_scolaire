import sqlite3
import os
from .database import CHEMIN_DB

class EleveRepository:
    @staticmethod
    def liste_complete():
        conn = sqlite3.connect(CHEMIN_DB)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM eleve ORDER BY nom, prenom")
        resultats = [dict(ligne) for ligne in cur.fetchall()]
        conn.close()
        return resultats

    @staticmethod
    def par_id(id_eleve):
        conn = sqlite3.connect(CHEMIN_DB)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM eleve WHERE id_eleve = ?", (id_eleve,))
        ligne = cur.fetchone()
        conn.close()
        return dict(ligne) if ligne else None

    @classmethod
    def total_verse(cls, id_eleve):
        conn = sqlite3.connect(CHEMIN_DB)
        cur = conn.cursor()
        cur.execute("SELECT COALESCE(SUM(montant_verse), 0) FROM paiement WHERE id_eleve = ?", (id_eleve,))
        total = cur.fetchone()[0]
        conn.close()
        return total

    @staticmethod
    def ajouter(nom, prenom, classe, annee_scolaire, montant_total_du):
        conn = sqlite3.connect(CHEMIN_DB)
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO eleve (nom, prenom, classe, annee_scolaire, montant_total_du)
            VALUES (?, ?, ?, ?, ?)
        """, (nom, prenom, classe, annee_scolaire, montant_total_du))
        conn.commit()
        conn.close()

    @staticmethod
    def modifier(id_eleve, nom, prenom, classe, annee_scolaire, montant_total_du):
        conn = sqlite3.connect(CHEMIN_DB)
        cur = conn.cursor()
        cur.execute("""
            UPDATE eleve
            SET nom=?, prenom=?, classe=?, annee_scolaire=?, montant_total_du=?
            WHERE id_eleve=?
        """, (nom, prenom, classe, annee_scolaire, montant_total_du, id_eleve))
        conn.commit()
        conn.close()

    @staticmethod
    def supprimer(id_eleve):
        conn = sqlite3.connect(CHEMIN_DB)
        cur = conn.cursor()
        cur.execute("DELETE FROM paiement WHERE id_eleve = ?", (id_eleve,))
        cur.execute("DELETE FROM eleve WHERE id_eleve = ?", (id_eleve,))
        conn.commit()
        conn.close()


class PaiementRepository:
    @staticmethod
    def historique(id_eleve):
        conn = sqlite3.connect(CHEMIN_DB)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("""
            SELECT * FROM paiement
            WHERE id_eleve = ?
            ORDER BY date_paiement DESC
        """, (id_eleve,))
        resultats = [dict(ligne) for ligne in cur.fetchall()]
        conn.close()
        return resultats

    @staticmethod
    def enregistrer(id_eleve, montant_verse, mode_paiement, date_paiement, numero_recu):
        conn = sqlite3.connect(CHEMIN_DB)
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO paiement (id_eleve, montant_verse, mode_paiement, date_paiement, numero_recu)
            VALUES (?, ?, ?, ?, ?)
        """, (id_eleve, montant_verse, mode_paiement, date_paiement, numero_recu))
        conn.commit()
        conn.close()
        return numero_recu