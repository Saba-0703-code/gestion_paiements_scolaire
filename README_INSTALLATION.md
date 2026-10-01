***
====================================================================
               EDUPAIE — GESTION DES PAIEMENTS SCOLAIRES
                      GUIDE D'INSTALLATION
====================================================================

## CONTENU DU DOSSIER
--------------------------------------------------------------------
Votre dossier contient :
   ├── EduPaie.exe          ← L'application (double-clic pour lancer)
   ├── 📁 data/             ← Base de données
   │     └── gestion_paiements.db
   ├── 📁 recus/            ← Reçus PDF générés (créé automatiquement)
   └── GUIDE_Installation.txt   ← Ce fichier

## INSTALLATION — Sur n'importe quel ordinateur
--------------------------------------------------------------------
1. Copier le dossier complet "EduPaie" sur le Bureau
2. Vérifier la structure :
      📁 EduPaie/
         ├── EduPaie.exe
         └── 📁 data/
              └── gestion_paiements.db
3. AUCUNE installation de Python n'est nécessaire ✅
4. AUCUNE commande à taper dans le terminal ✅

## LANCER L'APPLICATION
--------------------------------------------------------------------
→ Double-cliquer sur : EduPaie.exe
→ La fenêtre s'ouvre directement
→ Pas de fenêtre noire, pas d'invite de commande

## PREMIÈRE UTILISATION — Jeu de données de test
--------------------------------------------------------------------
La base est pré-remplie avec :
   • 15 élèves de CP1 à 4ème
   • Frais de scolarité de 75 000 à 145 000 FCFA
   • Statuts variés : Soldé / Partiellement payé / Non payé

Si la base est vide :
   → Exécuter "python data/jeu_test.py" dans le dossier du projet
   → Répondre "Oui" pour charger les données

## GÉNÉRER UN REÇU
--------------------------------------------------------------------
1. Ouvrir la fiche d'un élève (double-clic dans la liste)
2. Cliquer sur "➕ Enregistrer un versement"
3. Saisir le montant, la date et le mode de paiement
4. Valider → Le reçu PDF s'ouvre automatiquement
5. Le reçu est sauvegardé dans : 📁 recus/

## RÉ-IMPRESSION D'UN REÇU
--------------------------------------------------------------------
→ Ouvrir la fiche de l'élève → section "Historique des paiements"
→ Noter le numéro du reçu (ex: REC-20261001-143022)
→ Ouvrir le fichier correspondant dans 📁 recus/

## DÉPLACER L'APPLICATION SUR UNE CLÉ USB
--------------------------------------------------------------------
1. Copier tout le dossier "EduPaie" sur la clé
2. Branchez sur n'importe quel ordinateur
3. Double-cliquer sur EduPaie.exe → ça fonctionne immédiatement ✅

## QUESTIONS FRÉQUENTES
--------------------------------------------------------------------
Q : La base de données n'apparaît pas ?
R : Elle se crée automatiquement au premier lancement.

Q : Les reçus PDF ne s'ouvrent pas ?
R : Ils sont sauvegardés dans le dossier "recus/" à côté de EduPaie.exe.

Q : Puis-je installer l'application dans "Program Files" ?
R : De préférence sur le Bureau, pour que l'application puisse créer
     les dossiers "recus/" et accéder à la base de données.

Q : L'application est-elle gratuite ?
R : Oui, sous licence libre — à usage pédagogique.

## AUTEUR
====================================================================
   Développé par : SABA FELICIO
   Projet : Application de Gestion des Paiements Scolaires
   Date : 01/10/2026
   Version : 1.0
====================================================================