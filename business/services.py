from data.repositories import EleveRepository, PaiementRepository
from .recu_pdf import generer_recu_pdf
def obtenir_statut_eleve(id_eleve):
    """Retourne le statut : Soldé / Partiellement payé / Non payé"""
    eleve = EleveRepository.par_id(id_eleve)
    if not eleve:
        return "Inconnu"
    
    total_verse = EleveRepository.total_verse(id_eleve)
    if total_verse == 0:
        return "Non payé"
    if total_verse >= eleve["montant_total_du"]:
        return "Soldé"
    return "Partiellement payé"

def enregistrer_paiement_securise(id_eleve, montant, mode, date_paiement):
    """
    Enregistre un paiement avec vérification du solde.
    Retourne : (succès: bool, message: str, numero_recu: str|None)
    """
    eleve = EleveRepository.par_id(id_eleve)
    if not eleve:
        return False, "Élève introuvable", None, None
    
    total_verse = EleveRepository.total_verse(id_eleve)
    solde_restant = eleve["montant_total_du"] - total_verse
    
    if montant <= 0:
        return False, "Le montant doit être supérieur à 0", None
    if montant > solde_restant:
        return False, f"Montant trop élevé ! Solde restant : {solde_restant:,} FCFA", None
    
    # Générer numéro de reçu unique
    import datetime
    import time

    numero_recu = f"REC-{datetime.datetime.now().strftime('%Y%m%d-%H%M%S')}-{int(time.time() % 10000)}"
    
    PaiementRepository.enregistrer(
        id_eleve=id_eleve,
        montant_verse=montant,
        mode_paiement=mode,
        date_paiement=date_paiement,
        numero_recu=numero_recu
    )
    return True, "Paiement enregistré avec succès", numero_recu

def obtenir_donnees_tableau_de_bord():
    eleves = EleveRepository.liste_complete()
    nb_eleves = len(eleves)
    
    total_du = sum(e["montant_total_du"] for e in eleves)
    total_verse_global = 0
    nb_non_soldes = 0
    
    for e in eleves:
        vers = EleveRepository.total_verse(e["id_eleve"])  # ✅ e["id_eleve"] est bien passé
        total_verse_global += vers
        if vers < e["montant_total_du"]:
            nb_non_soldes += 1
    
    return {
        "nb_eleves": nb_eleves,
        "total_du": total_du,
        "total_verse": total_verse_global,
        "total_restant": total_du - total_verse_global,
        "nb_non_soldes": nb_non_soldes
    }


def enregistrer_paiement_securise(id_eleve, montant, mode, date_paiement):
    eleve = EleveRepository.par_id(id_eleve)
    if not eleve:
        return False, "Élève introuvable", None, None

    total_verse = EleveRepository.total_verse(id_eleve)
    solde_restant = eleve["montant_total_du"] - total_verse

    if montant <= 0:
        return False, "Le montant doit être supérieur à 0", None, None
    if montant > solde_restant:
        return False, f"Montant trop élevé ! Solde restant : {solde_restant:,} FCFA", None, None

    import datetime
    numero_recu = f"REC-{datetime.datetime.now().strftime('%Y%m%d-%H%M%S')}"

    PaiementRepository.enregistrer(
        id_eleve=id_eleve,
        montant_verse=montant,
        mode_paiement=mode,
        date_paiement=date_paiement,
        numero_recu=numero_recu
    )

    solde_apres = solde_restant - montant
    
    from .recu_pdf import generer_recu_pdf
    chemin_pdf = generer_recu_pdf(eleve, {
        "montant_verse": montant,
        "mode_paiement": mode,
        "date_paiement": date_paiement,
        "numero_recu": numero_recu
    }, solde_apres)

    return True, f"Paiement enregistré — Reçu N° {numero_recu}", numero_recu, chemin_pdf