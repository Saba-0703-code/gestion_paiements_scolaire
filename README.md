
---

```markdown
# Application de Gestion des Paiements Scolaires

Application de bureau pour suivre les frais et paiements des élèves dans les établissements scolaires. Plus de cahier de caisse papier : tout est automatisé, calculé et traçable.

---

## 📋 Fonctionnalités
-  Gestion des élèves (ajout, modification, suppression, recherche, filtre par classe)
-  Enregistrement des paiements avec validation du solde (interdit solde négatif)
-  Calcul automatique du solde et du statut : **Soldé / Partiellement payé / Non payé**
-  Historique complet des versements par élève
-  Génération de reçus PDF numérotés — ré-impression possible à tout moment
-  Tableau de bord avec indicateurs
-  Charte graphique : bleu unique + blanc + gris

---

##  Prérequis
- Python 3.10 ou supérieur

---

##  Installation

```bash
# 1. Se placer dans le dossier du projet
cd ~/Desktop/gestion_paiements_scolaire

# 2. Créer l'environnement virtuel
python -m venv .venv

# 3. Activer l'environnement
# Git Bash :
source .venv/Scripts/activate
# Windows CMD :
.venv\Scripts\activate.bat

# 4. Installer les dépendances
pip install -r requirements.txt
```

---

##  Lancement

```bash
python main.py
```

---

##  Charger le jeu de données de test (15 élèves)

```bash
python data/jeu_test.py
```
→ Répondre **`oui`** quand demandé.

---

## 📖 Manuel Utilisateur

### 1. Enregistrer un élève
1. Aller dans **Liste des élèves**
2. Cliquer sur **« Nouvel élève »**
3. Remplir : nom, prénom, classe, année scolaire, montant total des frais
4. Valider → l'élève apparaît dans la liste

### 2. Enregistrer un paiement
1. Cliquer sur le nom de l'élève dans la liste
2. Dans la fiche, cliquer sur **« ➕ Enregistrer un versement »**
3. Saisir : montant, date, mode de paiement
4. Valider → **le reçu PDF s'ouvre automatiquement**

>  Le montant ne peut pas dépasser le solde restant dû.

### 3. Voir ou ré-imprimer un reçu
1. Dans la fiche élève → Historique des paiements
2. Cliquer sur **« Voir reçu »**
3. Le PDF se génère dans le dossier `recus/` et s'ouvre immédiatement
4. Ré-imprimable à tout moment

### 4. Suivre les paiements
- **Recherche** : taper un nom dans la barre en haut
- **Filtre** : choisir une classe dans la liste déroulante
- **Statut** : Soldé / Partiellement payé / Non payé affiché dans la liste

---

## 🏗️ Architecture du projet

```
gestion_paiements_scolaire/
├── data/                ← Couche données
│   ├── database.py      ← Connexion & création tables
│   └── repositories.py  ← Requêtes SQL uniquement
├── business/            ← Couche métier
│   ├── services.py      ← Règles, calculs, validations
│   └── recu_pdf.py      ← Génération des reçus PDF
├── ui/                  ← Couche interface
│   ├── main_window.py
│   ├── eleve_form.py
│   ├── paiement_dialog.py
│   ├── fiche_eleve.py
│   └── tableau_bord.py
├── resources/           ← Style graphique QSS
├── recus/               ← Reçus PDF générés (auto-créé)
├── docs/                ← Documentation complémentaire
├── main.py              ← Point d'entrée
├── requirements.txt     ← Dépendances
└── README.md            ← Ce fichier
```

> **Règle d'or** : Aucune requête SQL dans le dossier `ui/` — tout passe par `data/` ✅

---

## 🗄️ Schéma de la base de données

Table :	Champs
eleve :	id_eleve, nom, prenom, classe, annee_scolaire, montant_total_du
paiement :	id_paiement, id_eleve (clé étrangère), date_paiement, montant_verse, mode_paiement, numero_recu (unique) 

### Règles de calcul
- **Solde restant** = montant_total_du − somme(montant_verse)
- **Statut Soldé** → solde = 0
- **Statut Partiellement payé** → solde > 0 et au moins 1 paiement
- **Statut Non payé** → aucun paiement

---

##  Charte Graphique
- Couleur principale : `#1565C0` (bleu)
- Fond : `#F5F7FA` (gris très clair)
- Texte : `#263238` (sombre)
- Pas de multicolore — sobriété et lisibilité

---

##  Choix Techniques
- **Langage** : Python 3 — simplicité, bibliothèques standard complètes
- **Interface** : PySide6 — composants natifs riches, multiplateforme
- **Base** : SQLite 
- **PDF** : fpdf2 --> contrôle total sur la mise en page
- **Architecture** : 3 couches séparées — maintenance facilitée

---

##  Limites connues
- Application **mono-utilisateur** (accès au fichier `.db` à tour de rôle)
- Pas de sauvegarde automatique → copier `data/gestion_paiements.db` régulièrement
- Pas de gestion des comptes utilisateurs

---

## 👤 Auteur
Projet réalisé dans le cadre de la formation **Développeur Web & Web Mobile**
```
