# Gestion des paiements scolaires

Application de bureau en Python pour gérer les élèves, les paiements, les soldes et les reçus de paiement dans un établissement scolaire.

## Présentation

Cette application permet de :

- enregistrer et consulter la liste des élèves ;
- suivre le montant total des frais ;
- enregistrer des versements ;
- calculer automatiquement le solde restant ;
- afficher le statut de chaque élève (non payé, partiellement payé, soldé) ;
- générer des reçus PDF.

Elle est développée avec PySide6 pour l'interface graphique et SQLite pour le stockage local des données.

## Fonctionnalités

- gestion des élèves ;
- ajout de paiements avec validation du montant ;
- calcul automatique du solde ;
- historique des versements ;
- génération de reçus PDF ;
- tableau de bord de synthèse ;
- interface ergonomique avec palette bleue et style personnalisé.

## Prérequis

- Python 3.10 ou plus récent ;
- un système d'exploitation compatible avec PySide6 (Windows, Linux, macOS).

## Installation

1. Placez-vous dans le dossier du projet :

```bash
cd chemin/vers/gestion_paiements_scolaire
```

2. Créez un environnement virtuel :

```bash
python -m venv .venv
```

3. Activez-le :

- Windows PowerShell :

```powershell
.venv\Scripts\Activate.ps1
```

- Windows CMD :

```cmd
.venv\Scripts\activate.bat
```

- Git Bash / bash Linux/macOS :

```bash
source .venv/Scripts/activate
```

4. Installez les dépendances :

```bash
pip install -r requirements.txt
```

## Lancement

```bash
python main.py
```

Le programme démarre la fenêtre principale et charge le style graphique prévu dans le dossier `resources`.

## Structure du projet

```text
gestion_paiements_scolaire/
├── business/
│   └── __init__.py
├── data/
│   ├── __init__.py
│   └── gestion_paiements.db
├── docs/
├── resources/
│   └── style.qss
├── ui/
│   ├── __init__.py
│   ├── fiche_eleve.py
│   ├── main_window.py
│   └── tableau_bord.py
├── .gitignore
├── main.py
├── README.md
├── requirements.txt
└── .venv/
```

## Base de données

Le projet utilise SQLite. La base est créée localement dans le dossier `data` et stocke les informations relatives aux élèves et aux paiements.

## Développement

Les fichiers principaux sont :

- `main.py` : point d'entrée de l'application ;
- `ui/main_window.py` : fenêtre principale et navigation ;
- `ui/fiche_eleve.py` : fiche détaillée d'un élève ;
- `ui/tableau_bord.py` : synthèse du tableau de bord ;
- `resources/style.qss` : style visuel de l'interface.

## Notes

- Le projet est conçu pour un usage local et mono-utilisateur.
- Les reçus PDF sont générés à partir des informations de paiement enregistrements.

## License

Ce projet est fourni sans licence spécifique dans le dépôt actuel.

## Auteur

<p align="center">
  <img src="resources/photo_auteur.png" alt="Photo de l'auteur" width="180" />
</p>

<h3 align="center">Saba Akouété Félicio</h3>

<p align="center">
  Développeur et concepteur du projet <strong>Gestion des paiements scolaires</strong>.
</p>

