# Etapes Futur

Ce document decrit la feuille de route recommandee pour faire evoluer Bybit Trade Journal depuis une application console Python vers une application desktop graphique moderne en HTML / CSS / JavaScript, tout en gardant le backend Python comme coeur du projet.

L'objectif final est :

- garder la logique metier actuelle en Python
- ajouter une interface graphique moderne
- faire tourner l'application localement comme une vraie app desktop
- preparer une livraison Windows avec un `.exe` et un installateur

## Vision cible

A terme, l'application doit proposer :

- un backend Python stable et reutilisable
- une interface graphique en HTML / CSS / JavaScript
- une fenetre desktop locale
- un stockage utilisateur propre
- un packaging Windows simple a installer

Technologies recommandees pour atteindre cet objectif :

- backend : Python
- interface : HTML / CSS / JavaScript
- shell desktop : PyWebView
- packaging : PyInstaller
- installateur Windows : Inno Setup

## Principes a respecter

Pour eviter de compliquer inutilement le projet, il faut garder ces regles :

- ne pas reecrire le backend actuel
- separer la logique metier de l'affichage console
- faire evoluer l'application par petites etapes testables
- garder une architecture simple
- preparer des chemins de fichiers compatibles avec une vraie installation Windows

## Roadmap recommandee

### Phase 1 - Stabiliser le backend pour une interface graphique

Objectif :
preparer le backend Python pour qu'il puisse etre utilise proprement par l'interface graphique desktop.

A faire :

- transformer les fonctions qui affichent encore directement avec `print` en fonctions qui renvoient des donnees propres
- faire renvoyer des `dict`, `list`, `bool` ou objets simples
- centraliser les erreurs dans des retours exploitables par une interface
- clarifier les chemins de `.env`, SQLite, exports et logs
- garder le backend independant de toute interface d'affichage

Resultat attendu :

- le backend devient independant de la console
- l'interface graphique pourra reutiliser directement la logique existante

### Phase 2 - Creer le shell desktop

Objectif :
ouvrir une vraie fenetre desktop locale sans encore refaire toute l'application.

A faire :

- ajouter un dossier `bybit_journal/desktop/`
- creer un fichier `main.py` qui ouvre une fenetre PyWebView
- charger une page HTML locale depuis `bybit_journal/frontend/`
- verifier que l'application s'ouvre sans terminal visible a terme

Resultat attendu :

- l'application devient une fenetre desktop
- la base technique de l'interface graphique existe

### Phase 3 - Creer le frontend de base

Objectif :
mettre en place une interface moderne simple en HTML / CSS / JavaScript.

A faire :

- creer `index.html`
- creer `styles.css`
- creer `app.js`
- creer une structure d'ecrans simple :
  - tableau de bord
  - liste des trades
  - statistiques
  - synchronisation
  - configuration API

Conseil :

- commencer en JavaScript simple, sans framework
- n'ajouter Vue ou React que si l'interface grossit plus tard

Resultat attendu :

- une interface visible et navigable
- une base solide pour brancher le backend

### Phase 4 - Faire le pont entre JavaScript et Python

Objectif :
relier les actions de l'interface graphique a la logique Python existante.

A faire :

- ajouter `bybit_journal/desktop/bridge.py`
- exposer des fonctions Python appelables depuis le frontend
- par exemple :
  - `get_trades(filters)`
  - `get_stats(filters)`
  - `sync_trades(days)`
  - `save_api_config(api_key, api_secret)`
  - `get_api_status()`

Resultat attendu :

- les boutons et formulaires du frontend pilotent vraiment l'application

### Phase 5 - Migrer progressivement les fonctions existantes vers la GUI

Objectif :
construire une interface utile sans tout refaire d'un coup.

Ordre recommande :

1. afficher les trades
2. ajouter les filtres
3. afficher les statistiques
4. ajouter la synchronisation Bybit
5. ajouter la configuration API
6. rebrancher l'export Excel

Resultat attendu :

- a chaque etape, l'application devient plus complete
- le projet reste testable en continu

### Phase 6 - Gerer proprement les donnees utilisateur

Objectif :
faire fonctionner l'application sur une autre machine Windows sans ecrire dans le dossier du programme.

A faire :

- stocker les donnees utilisateur dans des dossiers Windows adaptes
- separer le code de l'application et les fichiers utilisateur

Exemple de structure cible :

- `%APPDATA%/BybitTradeJournal/config/`
- `%APPDATA%/BybitTradeJournal/data/`
- `%USERPROFILE%/Documents/BybitTradeJournal/exports/`

Resultat attendu :

- l'application devient installable proprement
- les donnees utilisateur restent persistantes

### Phase 7 - Generer un executable Windows

Objectif :
creer un `.exe` utilisable sans lancer manuellement Python.

A faire :

- utiliser PyInstaller
- embarquer le code Python
- embarquer les fichiers HTML / CSS / JS
- embarquer les assets necessaires
- verifier le lancement sur une machine de test

Resultat attendu :

- premiere version executable de l'application

### Phase 8 - Gerer les prerequis Windows

Objectif :
assurer que l'application puisse s'executer sur la plupart des machines Windows.

Point cle :

- PyWebView utilise le moteur WebView du systeme
- sur Windows, il faut en pratique verifier la presence de WebView2

A faire :

- verifier si WebView2 est present
- sinon fournir une consigne ou un installateur de prerequis

Resultat attendu :

- moins d'erreurs au lancement sur les machines cibles

### Phase 9 - Creer un vrai installateur Windows

Objectif :
livrer l'application comme une vraie application desktop.

A faire :

- garder le build PyInstaller comme base
- ajouter un installateur avec Inno Setup
- creer des raccourcis
- choisir le dossier d'installation
- preparer les dossiers utilisateur

Resultat attendu :

- installation plus propre
- experience utilisateur proche d'une vraie application publiee

### Phase 10 - Finalisation produit

Objectif :
rendre l'application agreable, stable et partageable.

A faire :

- ajouter des etats de chargement
- ajouter des messages d'erreur propres
- ajouter des logs utiles
- definir une icone d'application
- gerer une version de l'application
- tester sur une machine Windows propre

Resultat attendu :

- application presentable
- application utilisable hors environnement de developpement

## Ordre concret conseille

Pour avancer efficacement, suivre cet ordre :

1. refactor du backend pour renvoyer des donnees propres
2. creation du shell PyWebView
3. creation du frontend HTML / CSS / JS
4. branchement de la lecture des trades
5. branchement des statistiques
6. branchement de la synchronisation
7. branchement de la configuration API
8. migration des fichiers utilisateur vers des dossiers Windows adaptes
9. packaging avec PyInstaller
10. creation de l'installateur Windows

## Architecture cible proposee

```text
crypto-trade-journal/
├─ .env
├─ requirements.txt
├─ README.md
├─ ETAPE_FUTUR.md
├─ packaging/
│  ├─ pyinstaller.spec
│  └─ installer/
└─ bybit_journal/
   ├─ src/
   │  ├─ api.py
   │  ├─ db.py
   │  ├─ sync.py
   │  ├─ config.py
   │  └─ services/
   ├─ desktop/
   │  ├─ main.py
   │  ├─ bridge.py
   │  └─ window.py
   ├─ frontend/
   │  ├─ index.html
   │  ├─ styles.css
   │  ├─ app.js
   │  └─ assets/
   ├─ data/
   └─ exports/
```

## Etat de depart conseille pour la suite

Avant de chercher a livrer une vraie application Windows, la prochaine milestone utile est :

- l'application s'ouvre dans une fenetre desktop
- les trades s'affichent dans l'interface
- les statistiques s'affichent
- la synchronisation Bybit fonctionne
- la configuration API fonctionne
- aucun usage du terminal n'est necessaire

Quand cette milestone est atteinte, le passage au `.exe` et a l'installateur devient beaucoup plus simple.
