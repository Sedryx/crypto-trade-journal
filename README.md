# Bybit Journal

Bybit Journal est une application CLI en Python qui recupere des executions depuis l'API Bybit, les stocke dans une base SQLite locale, puis permet de les consulter depuis un menu interactif.

Le projet est actuellement centre sur trois fonctions deja presentes :

- initialiser l'environnement local,
- configurer les credentials API Bybit,
- synchroniser et consulter les trades en base.

Les fonctionnalites non encore implementees ne sont pas documentees ici comme si elles existaient deja.

## Fonctionnalites actuelles

- creation automatique des dossiers de travail
- creation automatique du fichier `.env` si absent
- chargement des variables d'environnement Bybit
- initialisation de la base SQLite
- synchronisation des executions Bybit par categorie (`linear`, `spot`, `inverse`, `option`)
- prevention des doublons en base via `bybit_trade_id` unique
- affichage des trades stockes
- menu CLI simple pour piloter l'application

## Structure actuelle

```text
crypto-trade-journal/
|-- README.md
|-- requirements.txt
|-- todo.md
`-- bybit_journal/
    |-- data/
    |   `-- journal.db
    |-- src/
    |   |-- api.py
    |   |-- app.py
    |   |-- cli.py
    |   |-- config.py
    |   |-- db.py
    |   |-- export_exel.py
    |   |-- main.py
    |   |-- models.py
    |   `-- sync.py
    `-- tests/
        |-- dev_cli.py
        |-- dev_main.py
        `-- dev_tools.py
```

Notes :

- `export_exel.py` est present dans le depot mais n'est pas encore integre au flux principal.
- Les scripts dans `bybit_journal/tests/` servent aujourd'hui surtout d'outils de developpement.

## Prerequis

- Python 3.10 ou plus recent
- une cle API Bybit avec acces en lecture
- une connexion internet pour les appels API

Dependances Python actuelles :

- `requests`
- `python-dotenv`

## Installation

Creer un environnement virtuel puis installer les dependances :

```bash
pip install -r requirements.txt
```

## Configuration

Au premier lancement, le projet cree automatiquement un fichier `.env` a la racine du depot s'il n'existe pas.

Le menu permet ensuite de renseigner :

```env
BYBIT_API_KEY=your_api_key
BYBIT_API_SECRET=your_api_secret
```

## Lancement

Le point d'entree actuel est `bybit_journal/src/main.py`.

Depuis la racine du projet :

```bash
python bybit_journal/src/main.py
```

Le programme affiche un menu interactif avec ces options :

1. voir les trades
2. synchroniser les trades Bybit
3. configurer l'API Bybit
4. quitter

## Base de donnees

La base SQLite est stockee ici :

`bybit_journal/data/journal.db`

La table principale est `trades` et contient notamment :

- `bybit_trade_id`
- `symbol`
- `side`
- `qty`
- `entry_price`
- `exit_price`
- `pnl`
- `invested_amount`
- `trade_time`
- `note`
- `screenshot_path`

## Etat actuel du projet

Ce qui fonctionne deja :

- l'initialisation locale
- la configuration `.env`
- la lecture des credentials
- l'appel a l'API Bybit
- l'insertion SQLite
- l'evitement des doublons via `INSERT OR IGNORE`
- l'affichage des trades existants

Ce qui n'est pas encore branche dans le flux principal :

- export Excel
- ajout et edition de notes
- gestion des screenshots

## Limites actuelles

- la synchronisation recupere une fenetre recente et ne gere pas encore la pagination complete de l'API
- les scripts de dev ne constituent pas encore une vraie suite de tests automatisee complete
- le projet utilise aujourd'hui des imports simples depuis `src/`, adaptes a l'execution actuelle par script

## Avertissement

Ce projet est un journal de trading personnel a but educatif et organisationnel.
Il n'est pas affilie a Bybit.
