from data.database import get_connection
import datetime

class EleveRepository:
    @staticmethod
    def ajouter(nom, prenom, classe, annee_scolaire, montant_total_du):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO eleve (nom, prenom, classe, annee_scolaire, montant_total_du)
            VALUES (?, ?, ?, ?, ?)
        """, (nom, prenom, classe, annee_scolaire, montant_total_du))
        conn.commit()
        id_nouveau = cur.lastrowid
        conn.close()
        return id_nouveau

    @staticmethod
    def tous(recherche="", filtre_classe=""):
        conn = get_connection()
        cur = conn.cursor()
        sql = "SELECT * FROM vue_solde_eleve WHERE 1=1"
        params = []
        if recherche:
            sql += " AND (nom LIKE ? OR prenom LIKE ?)"
            params.extend([f"%{recherche}%", f"%{recherche}%"])
        if filtre_classe:
            sql += " AND classe = ?"
            params.append(filtre_classe)
        cur.execute(sql, params)
        resultats = cur.fetchall()
        conn.close()
        return [dict(ligne) for ligne in resultats]

    @staticmethod
    def par_id(id_eleve):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM vue_solde_eleve WHERE id_eleve = ?", (id_eleve,))
        ligne = cur.fetchone()
        conn.close()
        return dict(ligne) if ligne else None

    @staticmethod
    def modifier(id_eleve, nom, prenom, classe, annee_scolaire, montant_total_du):
        conn = get_connection()
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
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM eleve WHERE id_eleve = ?", (id_eleve,))
        conn.commit()
        conn.close()

    @staticmethod
    def liste_classes():
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT DISTINCT classe FROM eleve ORDER BY classe")
        resultats = [r[0] for r in cur.fetchall()]
        conn.close()
        return resultats


class PaiementRepository:
    @staticmethod
    def generer_numero_recu():
        """Génère numéro unique : RECU-AAAAMMJJ-XXXX"""
        date = datetime.date.today().strftime("%Y%m%d")
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT numero_recu FROM paiement WHERE numero_recu LIKE ?", (f"RECU-{date}-%",))
        existants = cur.fetchall()
        conn.close()
        numeros = [int(r[0].split("-")[-1]) for r in existants]
        prochain = max(numeros) + 1 if numeros else 1
        return f"RECU-{date}-{prochain:04d}"

    @staticmethod
    def enregistrer(id_eleve, montant_verse, mode_paiement, date_paiement=None):
        if date_paiement is None:
            date_paiement = datetime.date.today().strftime("%Y-%m-%d")
        numero = PaiementRepository.generer_numero_recu()
        
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO paiement (numero_recu, id_eleve, montant_verse, date_paiement, mode_paiement)
            VALUES (?, ?, ?, ?, ?)
        """, (numero, id_eleve, montant_verse, date_paiement, mode_paiement))
        conn.commit()
        conn.close()
        return numero

    @staticmethod
    def historique(id_eleve):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT * FROM paiement
            WHERE id_eleve = ?
            ORDER BY date_paiement DESC, id_paiement DESC
        """, (id_eleve,))
        resultats = cur.fetchall()
        conn.close()
        return [dict(ligne) for ligne in resultats]

    @staticmethod
    def par_numero_recu(numero_recu):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM paiement WHERE numero_recu = ?", (numero_recu,))
        ligne = cur.fetchone()
        conn.close()
        return dict(ligne) if ligne else None