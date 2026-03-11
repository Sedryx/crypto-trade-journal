# Bybit Trade Journal

Bybit Trade Journal est une application desktop locale pour synchroniser des executions Bybit, les stocker dans SQLite, analyser les statistiques du journal et exporter les trades en Excel.

L'application repose sur :

- un backend Python modulaire
- une interface desktop PyWebView
- un frontend local en HTML / CSS / JavaScript

## Fonctionnalites actuelles

- creation automatique des dossiers de travail
- creation automatique du fichier `.env` a la racine du projet
- chargement des cles API Bybit
- initialisation de la base SQLite
- synchronisation Bybit paginee par categorie
- synchronisation automatique au lancement de l'application
- prevention des doublons via `bybit_trade_id` unique
- dashboard wallet et resume du compte
- affichage du `Total equity`, des stablecoins et des autres actifs
- changement de devise d'affichage du wallet (`USD`, `JPY`, `GBP`, `CHF`, `EUR`)
- liste de trades avec filtres
- statistiques de base
- export Excel des trades filtres
- bouton de dev pour injecter des trades de test

## Structure

```text
crypto-trade-journal/
|-- README.md
|-- requirements.txt
|-- ETAPE_FUTUR.md
`-- bybit_journal/
    |-- desktop/
    |   |-- bridge.py
    |   |-- main.py
    |   `-- window.py
    |-- frontend/
    |   |-- app.js
    |   |-- index.html
    |   `-- styles.css
    |-- data/
    |   `-- journal.db
    |-- exports/
    |-- src/
    |   |-- api.py
    |   |-- config.py
    |   |-- db.py
    |   |-- models.py
    |   |-- sync.py
    |   `-- services/
    |       |-- __init__.py
    |       `-- journal_service.py
    `-- tests/
        `-- test_core.py
```

## Prerequis

- Python 3.13 recommande
- une cle API Bybit avec acces lecture
- une connexion internet pour les appels API

## Installation

Depuis la racine du projet :

```powershell
python -m pip install -r requirements.txt
```

Si tu utilises le venv du projet :

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Configuration

Au premier lancement, l'application cree automatiquement le fichier :

```text
/.env
```

avec :

```env
BYBIT_API_KEY=
BYBIT_API_SECRET=
```

Tu peux ensuite remplir les cles depuis l'ecran `Configuration` de l'application.

## Lancement

Le point d'entree de l'application est :

```text
bybit_journal/desktop/main.py
```

Commande :

```powershell
python bybit_journal/desktop/main.py
```

## Ecrans principaux

- `Dashboard` : etat API, wallet, resume du compte et trades recents
- `Trades` : filtres, table SQLite, export Excel et resume d'export
- `Synchronisation` : import Bybit sur une plage de jours
- `Statistiques` : PnL, win rate et indicateurs globaux
- `Configuration` : gestion du `.env` et bouton `DEV TEST ONLY`

## Export Excel

L'export Excel utilise les filtres de la vue `Trades` et cree un fichier `.xlsx` dans :

```text
bybit_journal/exports/
```

Le fichier contient :

- une feuille `Trades`
- une feuille `Stats`

## Comportement au lancement

Au demarrage :

- le backend Python initialise les dossiers, le `.env` et SQLite
- le frontend charge le dashboard, les trades et les statistiques
- si l'API Bybit est configuree, une synchronisation automatique se lance apres 1 seconde

## Tests

Lancer les tests :

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s bybit_journal/tests -p "test_*.py" -v
```

Verifier la compilation :

```powershell
.\.venv\Scripts\python.exe -m compileall bybit_journal/src bybit_journal/tests bybit_journal/desktop
```

## Limites actuelles

- l'application est orientee desktop local Windows
- le packaging final `.exe` + installateur n'est pas encore termine
- le bouton `DEV TEST ONLY` est present pour remplir rapidement la base en developpement

## Note

Projet personnel a but organisationnel et educatif. Non affilie a Bybit.
