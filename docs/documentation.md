
# Documentation Technique  Gestion des Paiements Scolaires

**Projet :** EduPaie

**Auteur :** Saba Akouété Félicio

**Date :** 30/09/2026

**Version :** 1.0

---

## 1. Présentation du Projet

### 1.1 Contexte
De nombreuses petites écoles et centres de formation n'ont pas de système informatisé de suivi des paiements. Le suivi se fait manuellement sur cahier ou fichier Excel, ce qui entraîne :
- Des calculs sujets à l'erreur
- L'absence de vue en temps réel sur les sommes dues
- La difficulté à produire un reçu fiable et numéroté

### 1.2 Objectif
Développer une application de bureau qui permet :
- D'enregistrer les élèves et leurs frais de scolarité
- D'enregistrer chaque paiement au fur et à mesure
- De calculer automatiquement le solde restant
- De générer un reçu PDF numéroté à chaque versement
- De fournir une vue d'ensemble via un tableau de bord

### 1.3 Public cible
Secrétaires et gestionnaires d'établissements, sans compétences techniques particulières.

---

## 2. Architecture du Système

### 2.1 Structure en Couches
L'application respecte une architecture en **3 couches distinctes** :

| Couche | Dossier | Rôle |
|---|---|---|
| **Données** | `data/` | Connexion SQLite, schéma, requêtes SQL |
| **Métier** | `business/` | Règles de gestion, calculs, validations |
| **Interface** | `ui/` | Fenêtres, formulaires, dialogue — **aucune requête SQL ici** |

### 2.2 Diagramme des Dépendances
```
main.py
  ├── ui/ (interface)
  │     └── business/ (règles)
  │           └── data/ (accès base)
  └── resources/ (style, images)
```

### 2.3 Choix Justifiés
- **Séparation des couches** : facilite la maintenance, le test et l'évolution
- **SQLite** : fichier unique, pas de serveur nécessaire, adapté pour une application mono-poste
- **PySide6** : bibliothèque mature, composants natifs, multiplateforme
- **fpdf2** : contrôle total sur la mise en page des reçus PDF

---

## 3. Modélisation des Données

### 3.1 Schéma de la Base

#### Table `eleve`
| Champ | Type | Contrainte |
|---|---|---|
| `id_eleve` | INTEGER | Clé primaire, auto-incrément |
| `nom` | TEXT | Non null |
| `prenom` | TEXT | Non null |
| `classe` | TEXT | Non null |
| `annee_scolaire` | TEXT | Non null |
| `montant_total_du` | REAL | ≥ 0 |

#### Table `paiement`
| Champ | Type | Contrainte |
|---|---|---|
| `id_paiement` | INTEGER | Clé primaire |
| `id_eleve` | INTEGER | Clé étrangère → `eleve` |
| `date_paiement` | TEXT | Format ISO |
| `montant_verse` | REAL | > 0 |
| `mode_paiement` | TEXT | espèces/chèque/virement/mobile_money |
| `numero_recu` | TEXT | Unique |

### 3.2 Règles de Gestion
- **Solde restant** = `montant_total_du` − somme des `montant_verse`
- **Statut** :
  - Non payé → aucun paiement enregistré
  - Partiellement payé → solde > 0 et au moins un versement
  - Soldé → solde = 0
- **Interdiction** : un paiement ne peut faire passer le solde en dessous de 0

---

## 4. Fonctionnalités Détaillées

### 4.1 Gestion des Élèves
- Ajout avec validation des champs obligatoires
- Modification des informations
- Suppression avec confirmation
- Recherche par nom/prénom
- Filtre par classe
- Affichage du statut de paiement dans la liste

### 4.2 Enregistrement des Paiements
- Formulaire avec date par défaut = aujourd'hui
- Contrôle en temps réel : montant ≤ solde restant
- Génération automatique du numéro de reçu
- Message de confirmation avec numéro du reçu

### 4.3 Génération des Reçus
- Format PDF structuré
- Numéro unique persistant
- Informations complètes : identité, montant, mode, solde après versement
- Ré-impression possible depuis l'historique

### 4.4 Tableau de Bord
- Nombre total d'élèves
- Montant total attendu / perçu / restant
- Nombre d'élèves non soldés
- Pourcentage de recouvrement

---

## 5. Interface Utilisateur

### 5.1 Charte Graphique
- Couleur principale : `#1565C0` (bleu)
- Fond : `#F5F7FA`
- Texte : `#263238`
- Police : système par défaut (lisibilité)
- Style centralisé dans `resources/style.qss`

### 5.2 Écrans Principaux
- Accueil → Tableau de bord
- Liste → Recherche, filtre, actions
- Fiche élève → Informations, solde, historique, actions
- Dialogue → Saisie paiement

---

## 6. Installation et Déploiement

```bash
# 1. Récupération du projet
git clone https://github.com/Saba-0703-code/gestion_paiements_scolaire.git
cd gestion_paiements_scolaire

# 2. Environnement
python -m venv .venv
source .venv/Scripts/activate  # Windows : .venv\Scripts\activate.bat

# 3. Dépendances
pip install -r requirements.txt

# 4. Données de test
python data/jeu_test.py

# 5. Lancement
python main.py
```

---

## 7. Limites Connues et Perspectives

### 7.1 Limites Actuelles
- Application **mono-utilisateur** : accès exclusif au fichier `.db`
- Pas de sauvegarde automatique → copie manuelle recommandée
- Pas de gestion de comptes utilisateurs / droits d'accès
- Pas de synchronisation réseau

### 7.2 Perspectives d'Évolution
- Gestion multi-utilisateurs avec verrouillage
- Sauvegarde automatique vers dossier externe
- Export des données (Excel / CSV)
- Gestion des frais par période / par trimestre
- Graphiques d'évolution des encaissements

---

## 8. Références
- **Python** : https://docs.python.org/3/
- **PySide6** : https://doc.qt.io/qtforpython/
- **SQLite** : https://www.sqlite.org/docs.html
- **fpdf2** : https://pyfpdf.github.io/fpdf2/
```

---

##  ÉTAPE 3 — Créer le manuel utilisateur (1 page)

Crée `docs/manuel_utilisateur.md` :

```markdown
# Manuel Utilisateur — EduPaie

##  Lancement
Double-cliquez sur `main.py` ou tapez :
```bash
python main.py
```

## 1. Enregistrer un élève
1. Aller dans **Liste des élèves**
2. Cliquer sur **« Nouvel élève »**
3. Remplir : nom, prénom, classe, année, montant total des frais
4. Valider → l'élève apparaît dans la liste

## 2. Enregistrer un paiement
1. Cliquer sur le nom de l'élève
2. Dans la fiche → **« Enregistrer un versement »**
3. Saisir : montant, date, mode de paiement
4. Valider → le reçu s'ouvre automatiquement

> ⚠️ Le montant ne peut pas dépasser ce qui reste à payer.

## 3. Consulter ou ré-imprimer un reçu
1. Ouvrir la fiche de l'élève
2. Descendre à **Historique des paiements**
3. Cliquer sur **« Voir reçu »** sur la ligne concernée
4. Le PDF s'ouvre → imprimer ou sauvegarder

## 4. Suivre les paiements
- **Recherche** : taper un nom dans la barre en haut
- **Filtre** : choisir une classe dans la liste
- **Statut** : Soldé / Partiellement payé / Non payé → directement dans la liste
- **Tableau de bord** : vue d'ensemble à l'accueil

## 5. Conseils
- Fermer l'application après usage
- Copier régulièrement `data/gestion_paiements.db` en lieu sûr
- Les reçus sont conservés dans le dossier `recus/`
```

---

##  ÉTAPE 4 — Ajouter tout dans Git et pousser

```bash
git add docs/
git commit -m "Ajout documentation complète"
git push origin main
`