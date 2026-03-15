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

cd .\.venv\Scripts\ 
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\Activate.ps1
cd ..\..\bybit_journal\desktop\
python .\main.py

rebuild :

powershell -ExecutionPolicy Bypass -File ..\..\packaging\build_windows.ps1 -Clean


Trade notes editing
This is the most natural upgrade for a journal app.
Trade detail panel
Clicking a row should show full trade info cleanly.
Delete confirmation
Small change, big UX win.
Open folder actions
Open exports folder, open config folder, maybe open database folder.
Sync settings
Let the user choose startup sync on/off and default sync window.
Backup / restore
A simple SQLite backup feature would make the app feel much safer.

screenshots
charts everywhere
multi-exchange support
cloud sync
overly advanced analytics

Good upgrades later
These are good, but not the next thing I’d do:

charts
screenshots
multi-exchange support
advanced performance analytics
tagging systems
full onboarding wizard
Those are nice, but they’ll increase complexity fast.

Biggest architectural risk
The biggest risk isn’t the code quality. It’s drift:

docs say one thing
repo contains old runtime files
packaged app uses another storage model
dev helpers are still visible in the UI




:
(.venv) PS C:\Users\joach\OneDrive - EDUETATFR\Documents\Moi\crypto-trade-journal\bybit_journal\desktop> python .\main.py
[pywebview] Using WinForms / Chromium
[pywebview] before_load event fired. injecting pywebview object
[pywebview] Loading JS files from C:\Users\joach\OneDrive - EDUETATFR\Documents\Moi\crypto-trade-journal\.venv\Lib\site-packages\webview\js
[pywebview] _pywebviewready event fired
[pywebview] loaded event fired
(.venv) PS C:\Users\joach\OneDrive - EDUETATFR\Documents\Moi\crypto-trade-journal\bybit_journal\desktop> powershell -ExecutionPolicy Bypass -File ..\..\packaging\build_windows.ps1 -Clean
>>
128 INFO: PyInstaller: 6.19.0, contrib hooks: 2026.3
128 INFO: Python: 3.13.12
146 INFO: Platform: Windows-11-10.0.26200-SP0
146 INFO: Python environment: C:\Users\joach\OneDrive - EDUETATFR\Documents\Moi\crypto-trade-journal\.venv
107 WARNING: Failed to collect submodules for 'webview.platforms.android' because importing 'webview.platforms.android' raised: ModuleNotFoundError: No module named 'android'
923 INFO: Module search paths (PYTHONPATH):
['C:\\Users\\joach\\OneDrive - EDUETATFR\\Documents\\Moi\\crypto-trade-journal',
 'C:\\Users\\joach\\AppData\\Local\\Python\\pythoncore-3.13-64\\python313.zip',
 'C:\\Users\\joach\\AppData\\Local\\Python\\pythoncore-3.13-64\\DLLs',
 'C:\\Users\\joach\\AppData\\Local\\Python\\pythoncore-3.13-64\\Lib',
 'C:\\Users\\joach\\AppData\\Local\\Python\\pythoncore-3.13-64',
 'C:\\Users\\joach\\OneDrive - '
 'EDUETATFR\\Documents\\Moi\\crypto-trade-journal\\.venv',
 'C:\\Users\\joach\\OneDrive - '
 'EDUETATFR\\Documents\\Moi\\crypto-trade-journal\\.venv\\Lib\\site-packages',
 'C:\\Users\\joach\\OneDrive - '
 'EDUETATFR\\Documents\\Moi\\crypto-trade-journal\\bybit_journal\\desktop',
 'C:\\Users\\joach\\OneDrive - EDUETATFR\\Documents\\Moi\\crypto-trade-journal',
 'C:\\Users\\joach\\OneDrive - '
 'EDUETATFR\\Documents\\Moi\\crypto-trade-journal\\bybit_journal\\src']
1199 INFO: Appending 'datas' from .spec
1201 INFO: checking Analysis
1202 INFO: Building Analysis because Analysis-00.toc is non existent
1202 INFO: Looking for Python shared library...
1202 INFO: Using Python shared library: C:\Users\joach\AppData\Local\Python\pythoncore-3.13-64\python313.dll
1202 INFO: Running Analysis Analysis-00.toc
1202 INFO: Target bytecode optimization level: 0
1202 INFO: Initializing module dependency graph...
1203 INFO: Initializing module graph hook caches...
1218 INFO: Analyzing modules for base_library.zip ...
2262 INFO: Processing standard module hook 'hook-encodings.py' from 'C:\\Users\\joach\\OneDrive - EDUETATFR\\Documents\\Moi\\crypto-trade-journal\\.venv\\Lib\\site-packages\\PyInstaller\\hooks'
2835 INFO: Processing standard module hook 'hook-heapq.py' from 'C:\\Users\\joach\\OneDrive - EDUETATFR\\Documents\\Moi\\crypto-trade-journal\\.venv\\Lib\\site-packages\\PyInstaller\\hooks'
3698 INFO: Processing standard module hook 'hook-pickle.py' from 'C:\\Users\\joach\\OneDrive - EDUETATFR\\Documents\\Moi\\crypto-trade-journal\\.venv\\Lib\\site-packages\\PyInstaller\\hooks'
4648 INFO: Caching module dependency graph...
4671 INFO: Analyzing C:\Users\joach\OneDrive - EDUETATFR\Documents\Moi\crypto-trade-journal\bybit_journal\desktop\main.py
4728 INFO: Processing standard module hook 'hook-xml.py' from 'C:\\Users\\joach\\OneDrive - EDUETATFR\\Documents\\Moi\\crypto-trade-journal\\.venv\\Lib\\site-packages\\PyInstaller\\hooks'
4743 INFO: Processing standard module hook 'hook-xml.etree.cElementTree.py' from 'C:\\Users\\joach\\OneDrive - EDUETATFR\\Documents\\Moi\\crypto-trade-journal\\.venv\\Lib\\site-packages\\PyInstaller\\hooks'
4785 INFO: Processing standard module hook 'hook-urllib3.py' from 'C:\\Users\\joach\\OneDrive - EDUETATFR\\Documents\\Moi\\crypto-trade-journal\\.venv\\Lib\\site-packages\\_pyinstaller_hooks_contrib\\stdhooks'
4923 INFO: Processing pre-safe-import-module hook 'hook-backports.py' from 'C:\\Users\\joach\\OneDrive - EDUETATFR\\Documents\\Moi\\crypto-trade-journal\\.venv\\Lib\\site-packages\\PyInstaller\\hooks\\pre_safe_import_module'
4924 INFO: SetuptoolsInfo: initializing cached setuptools info...
5486 INFO: Setuptools: 'backports' appears to be a full setuptools-vendored copy - creating alias to 'setuptools._vendor.backports'!
5491 INFO: Processing standard module hook 'hook-setuptools.py' from 'C:\\Users\\joach\\OneDrive - EDUETATFR\\Documents\\Moi\\crypto-trade-journal\\.venv\\Lib\\site-packages\\PyInstaller\\hooks'
5527 INFO: Processing standard module hook 'hook-platform.py' from 'C:\\Users\\joach\\OneDrive - EDUETATFR\\Documents\\Moi\\crypto-trade-journal\\.venv\\Lib\\site-packages\\PyInstaller\\hooks'
5556 INFO: Processing standard module hook 'hook-sysconfig.py' from 'C:\\Users\\joach\\OneDrive - EDUETATFR\\Documents\\Moi\\crypto-trade-journal\\.venv\\Lib\\site-packages\\PyInstaller\\hooks'
5560 INFO: Processing standard module hook 'hook-_ctypes.py' from 'C:\\Users\\joach\\OneDrive - EDUETATFR\\Documents\\Moi\\crypto-trade-journal\\.venv\\Lib\\site-packages\\PyInstaller\\hooks'
5566 INFO: Processing pre-safe-import-module hook 'hook-distutils.py' from 'C:\\Users\\joach\\OneDrive - EDUETATFR\\Documents\\Moi\\crypto-trade-journal\\.venv\\Lib\\site-packages\\PyInstaller\\hooks\\pre_safe_import_module'
5592 INFO: Processing pre-safe-import-module hook 'hook-jaraco.py' from 'C:\\Users\\joach\\OneDrive - EDUETATFR\\Documents\\Moi\\crypto-trade-journal\\.venv\\Lib\\site-packages\\PyInstaller\\hooks\\pre_safe_import_module'
5592 INFO: Setuptools: 'jaraco' appears to be a full setuptools-vendored copy - creating alias to 'setuptools._vendor.jaraco'!
5601 INFO: Processing pre-safe-import-module hook 'hook-more_itertools.py' from 'C:\\Users\\joach\\OneDrive - EDUETATFR\\Documents\\Moi\\crypto-trade-journal\\.venv\\Lib\\site-packages\\PyInstaller\\hooks\\pre_safe_import_module'
5601 INFO: Setuptools: 'more_itertools' appears to be a setuptools-vendored copy - creating alias to 'setuptools._vendor.more_itertools'!
5707 INFO: Processing pre-safe-import-module hook 'hook-typing_extensions.py' from 'C:\\Users\\joach\\OneDrive - EDUETATFR\\Documents\\Moi\\crypto-trade-journal\\.venv\\Lib\\site-packages\\PyInstaller\\hooks\\pre_safe_import_module'
5918 INFO: Processing standard module hook 'hook-multiprocessing.util.py' from 'C:\\Users\\joach\\OneDrive - EDUETATFR\\Documents\\Moi\\crypto-trade-journal\\.venv\\Lib\\site-packages\\PyInstaller\\hooks'
6490 INFO: Processing pre-safe-import-module hook 'hook-packaging.py' from 'C:\\Users\\joach\\OneDrive - EDUETATFR\\Documents\\Moi\\crypto-trade-journal\\.venv\\Lib\\site-packages\\PyInstaller\\hooks\\pre_safe_import_module'
6618 INFO: Processing standard module hook 'hook-setuptools._vendor.jaraco.text.py' from 'C:\\Users\\joach\\OneDrive - EDUETATFR\\Documents\\Moi\\crypto-trade-journal\\.venv\\Lib\\site-packages\\PyInstaller\\hooks'
6620 INFO: Processing pre-safe-import-module hook 'hook-importlib_resources.py' from 'C:\\Users\\joach\\OneDrive - EDUETATFR\\Documents\\Moi\\crypto-trade-journal\\.venv\\Lib\\site-packages\\PyInstaller\\hooks\\pre_safe_import_module'
6917 INFO: Processing pre-safe-import-module hook 'hook-importlib_metadata.py' from 'C:\\Users\\joach\\OneDrive - EDUETATFR\\Documents\\Moi\\crypto-trade-journal\\.venv\\Lib\\site-packages\\PyInstaller\\hooks\\pre_safe_import_module'
6918 INFO: Setuptools: 'importlib_metadata' appears to be a setuptools-vendored copy - creating alias to 'setuptools._vendor.importlib_metadata'!
6936 INFO: Processing standard module hook 'hook-setuptools._vendor.importlib_metadata.py' from 'C:\\Users\\joach\\OneDrive - EDUETATFR\\Documents\\Moi\\crypto-trade-journal\\.venv\\Lib\\site-packages\\PyInstaller\\hooks'
6956 INFO: Processing pre-safe-import-module hook 'hook-zipp.py' from 'C:\\Users\\joach\\OneDrive - EDUETATFR\\Documents\\Moi\\crypto-trade-journal\\.venv\\Lib\\site-packages\\PyInstaller\\hooks\\pre_safe_import_module'
6956 INFO: Setuptools: 'zipp' appears to be a setuptools-vendored copy - creating alias to 'setuptools._vendor.zipp'!
7141 INFO: Processing pre-safe-import-module hook 'hook-tomli.py' from 'C:\\Users\\joach\\OneDrive - EDUETATFR\\Documents\\Moi\\crypto-trade-journal\\.venv\\Lib\\site-packages\\PyInstaller\\hooks\\pre_safe_import_module'
7142 INFO: Setuptools: 'tomli' appears to be a setuptools-vendored copy - creating alias to 'setuptools._vendor.tomli'!
7548 INFO: Processing pre-safe-import-module hook 'hook-wheel.py' from 'C:\\Users\\joach\\OneDrive - EDUETATFR\\Documents\\Moi\\crypto-trade-journal\\.venv\\Lib\\site-packages\\PyInstaller\\hooks\\pre_safe_import_module'
7549 INFO: Setuptools: 'wheel' appears to be a setuptools-vendored copy - creating alias to 'setuptools._vendor.wheel'!
7947 INFO: Processing standard module hook 'hook-charset_normalizer.py' from 'C:\\Users\\joach\\OneDrive - EDUETATFR\\Documents\\Moi\\crypto-trade-journal\\.venv\\Lib\\site-packages\\_pyinstaller_hooks_contrib\\stdhooks'
8065 INFO: Processing standard module hook 'hook-certifi.py' from 'C:\\Users\\joach\\OneDrive - EDUETATFR\\Documents\\Moi\\crypto-trade-journal\\.venv\\Lib\\site-packages\\_pyinstaller_hooks_contrib\\stdhooks'
8155 INFO: Processing standard module hook 'hook-sqlite3.py' from 'C:\\Users\\joach\\OneDrive - EDUETATFR\\Documents\\Moi\\crypto-trade-journal\\.venv\\Lib\\site-packages\\PyInstaller\\hooks'
8434 INFO: Processing standard module hook 'hook-openpyxl.py' from 'C:\\Users\\joach\\OneDrive - EDUETATFR\\Documents\\Moi\\crypto-trade-journal\\.venv\\Lib\\site-packages\\_pyinstaller_hooks_contrib\\stdhooks'
9431 INFO: Processing standard module hook 'hook-webview.py' from 'C:\\Users\\joach\\OneDrive - EDUETATFR\\Documents\\Moi\\crypto-trade-journal\\.venv\\Lib\\site-packages\\webview\\__pyinstaller'
9984 INFO: Processing pre-safe-import-module hook 'hook-gi.py' from 'C:\\Users\\joach\\OneDrive - EDUETATFR\\Documents\\Moi\\crypto-trade-journal\\.venv\\Lib\\site-packages\\PyInstaller\\hooks\\pre_safe_import_module'
10114 INFO: Processing standard module hook 'hook-clr.py' from 'C:\\Users\\joach\\OneDrive - EDUETATFR\\Documents\\Moi\\crypto-trade-journal\\.venv\\Lib\\site-packages\\_pyinstaller_hooks_contrib\\stdhooks'
10127 INFO: Processing standard module hook 'hook-clr_loader.py' from 'C:\\Users\\joach\\OneDrive - EDUETATFR\\Documents\\Moi\\crypto-trade-journal\\.venv\\Lib\\site-packages\\_pyinstaller_hooks_contrib\\stdhooks'
10223 INFO: Processing standard module hook 'hook-pycparser.py' from 'C:\\Users\\joach\\OneDrive - EDUETATFR\\Documents\\Moi\\crypto-trade-journal\\.venv\\Lib\\site-packages\\_pyinstaller_hooks_contrib\\stdhooks'
10713 INFO: Processing standard module hook 'hook-difflib.py' from 'C:\\Users\\joach\\OneDrive - EDUETATFR\\Documents\\Moi\\crypto-trade-journal\\.venv\\Lib\\site-packages\\PyInstaller\\hooks'
11002 INFO: Analyzing hidden import 'webview.__pyinstaller'
11003 INFO: Analyzing hidden import 'webview.__pyinstaller.hook-webview'
11028 INFO: Processing standard module hook 'hook-win32ctypes.core.py' from 'C:\\Users\\joach\\OneDrive - EDUETATFR\\Documents\\Moi\\crypto-trade-journal\\.venv\\Lib\\site-packages\\PyInstaller\\hooks'
12117 INFO: Analyzing hidden import 'webview._version'
12118 INFO: Analyzing hidden import 'openpyxl.compat.abc'
12119 INFO: Analyzing hidden import 'openpyxl.compat.product'
12120 INFO: Analyzing hidden import 'openpyxl.compat.singleton'
12121 INFO: Analyzing hidden import 'openpyxl.descriptors.slots'
12123 INFO: Analyzing hidden import 'openpyxl.packaging.interface'
12124 INFO: Analyzing hidden import 'openpyxl.utils.dataframe'
12127 INFO: Analyzing hidden import 'openpyxl.utils.inference'
12129 INFO: Analyzing hidden import 'openpyxl.worksheet.cell_watch'
12130 INFO: Analyzing hidden import 'openpyxl.worksheet.controls'
12137 INFO: Analyzing hidden import 'openpyxl.worksheet.custom'
12139 INFO: Analyzing hidden import 'openpyxl.worksheet.errors'
12141 INFO: Analyzing hidden import 'openpyxl.worksheet.picture'
12142 INFO: Analyzing hidden import 'openpyxl.worksheet.smart_tag'
12145 INFO: Processing module hooks (post-graph stage)...
12146 WARNING: Hidden import "pycparser.lextab" not found!
12146 WARNING: Hidden import "pycparser.yacctab" not found!
12242 INFO: Performing binary vs. data reclassification (33 entries)
12254 INFO: Looking for ctypes DLLs
12294 INFO: Analyzing run-time hooks ...
12297 INFO: Including run-time hook 'pyi_rth_inspect.py' from 'C:\\Users\\joach\\OneDrive - EDUETATFR\\Documents\\Moi\\crypto-trade-journal\\.venv\\Lib\\site-packages\\PyInstaller\\hooks\\rthooks'
12299 INFO: Including run-time hook 'pyi_rth_pkgutil.py' from 'C:\\Users\\joach\\OneDrive - EDUETATFR\\Documents\\Moi\\crypto-trade-journal\\.venv\\Lib\\site-packages\\PyInstaller\\hooks\\rthooks'
12301 INFO: Including run-time hook 'pyi_rth_multiprocessing.py' from 'C:\\Users\\joach\\OneDrive - EDUETATFR\\Documents\\Moi\\crypto-trade-journal\\.venv\\Lib\\site-packages\\PyInstaller\\hooks\\rthooks'
12303 INFO: Including run-time hook 'pyi_rth_setuptools.py' from 'C:\\Users\\joach\\OneDrive - EDUETATFR\\Documents\\Moi\\crypto-trade-journal\\.venv\\Lib\\site-packages\\PyInstaller\\hooks\\rthooks'
12309 INFO: Creating base_library.zip...
12328 INFO: Looking for dynamic libraries
12934 INFO: Extra DLL search directories (AddDllDirectory): []
12934 INFO: Extra DLL search directories (PATH): []
13213 INFO: Warnings written to C:\Users\joach\OneDrive - EDUETATFR\Documents\Moi\crypto-trade-journal\build\pyinstaller\warn-pyinstaller.txt
13261 INFO: Graph cross-reference written to C:\Users\joach\OneDrive - EDUETATFR\Documents\Moi\crypto-trade-journal\build\pyinstaller\xref-pyinstaller.html
13287 INFO: checking PYZ
13287 INFO: Building PYZ because PYZ-00.toc is non existent
13287 INFO: Building PYZ (ZlibArchive) C:\Users\joach\OneDrive - EDUETATFR\Documents\Moi\crypto-trade-journal\build\pyinstaller\PYZ-00.pyz
13764 INFO: Building PYZ (ZlibArchive) C:\Users\joach\OneDrive - EDUETATFR\Documents\Moi\crypto-trade-journal\build\pyinstaller\PYZ-00.pyz completed successfully.
13781 INFO: checking PKG
13781 INFO: Building PKG because PKG-00.toc is non existent
13781 INFO: Building PKG (CArchive) BybitTradeJournal.pkg
13794 INFO: Building PKG (CArchive) BybitTradeJournal.pkg completed successfully.
13795 INFO: Bootloader C:\Users\joach\OneDrive - EDUETATFR\Documents\Moi\crypto-trade-journal\.venv\Lib\site-packages\PyInstaller\bootloader\Windows-64bit-intel\runw.exe
13795 INFO: checking EXE
13795 INFO: Building EXE because EXE-00.toc is non existent
13795 INFO: Building EXE from EXE-00.toc
13795 INFO: Copying bootloader EXE to C:\Users\joach\OneDrive - EDUETATFR\Documents\Moi\crypto-trade-journal\build\pyinstaller\BybitTradeJournal.exe
13799 INFO: Copying icon to EXE
Traceback (most recent call last):
  File "C:\Users\joach\OneDrive - EDUETATFR\Documents\Moi\crypto-trade-journal\.venv\Lib\site-packages\PyInstaller\building\icon.py", line 50, in normalize_icon_type
    from PIL import Image as PILImage
ModuleNotFoundError: No module named 'PIL'

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "<frozen runpy>", line 198, in _run_module_as_main
  File "<frozen runpy>", line 88, in _run_code
  File "C:\Users\joach\OneDrive - EDUETATFR\Documents\Moi\crypto-trade-journal\.venv\Lib\site-packages\PyInstaller\__main__.py", line 321, in <module>
    run()
    ~~~^^
  File "C:\Users\joach\OneDrive - EDUETATFR\Documents\Moi\crypto-trade-journal\.venv\Lib\site-packages\PyInstaller\__main__.py", line 215, in run
    run_build(pyi_config, spec_file, **vars(args))
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\joach\OneDrive - EDUETATFR\Documents\Moi\crypto-trade-journal\.venv\Lib\site-packages\PyInstaller\__main__.py", line 70, in run_build
    PyInstaller.building.build_main.main(pyi_config, spec_file, **kwargs)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\joach\OneDrive - EDUETATFR\Documents\Moi\crypto-trade-journal\.venv\Lib\site-packages\PyInstaller\building\build_main.py", line 1275, in main
    build(specfile, distpath, workpath, clean_build)
    ~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\joach\OneDrive - EDUETATFR\Documents\Moi\crypto-trade-journal\.venv\Lib\site-packages\PyInstaller\building\build_main.py", line 1213, in build
    exec(code, spec_namespace)
    ~~~~^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\joach\OneDrive - EDUETATFR\Documents\Moi\crypto-trade-journal\packaging\\pyinstaller.spec", line 38, in <module>
    exe = EXE(
        pyz,
    ...<11 lines>...
        icon=str(APP_ICON),
    )
  File "C:\Users\joach\OneDrive - EDUETATFR\Documents\Moi\crypto-trade-journal\.venv\Lib\site-packages\PyInstaller\building\api.py", line 675, in __init__
    ~~~~~~~~~~~~~~~~~^^
    ~~~~~~~~~~~~~~~~~^^
  File "C:\Users\joach\OneDrive - EDUETATFR\Documents\Moi\crypto-trade-journal\.venv\Lib\site-packages\PyInstaller\building\datastruct.py", line 184, in __postinit__
    self.assemble()
    ~~~~~~~~~~~~~^^
  File "C:\Users\joach\OneDrive - EDUETATFR\Documents\Moi\crypto-trade-journal\.venv\Lib\site-packages\PyInstaller\building\api.py", line 788, in assemble
    self._retry_operation(icon.CopyIcons, build_name, self.icon)
    ~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\joach\OneDrive - EDUETATFR\Documents\Moi\crypto-trade-journal\.venv\Lib\site-packages\PyInstaller\building\api.py", line 1058, in _retry_operation
    return func(*args)
  File "C:\Users\joach\OneDrive - EDUETATFR\Documents\Moi\crypto-trade-journal\.venv\Lib\site-packages\PyInstaller\utils\win32\icon.py", line 206, in CopyIcons
    srcpath = normalize_icon_type(srcpath, ("exe", "ico"), "ico", config.CONF["workpath"])
  File "C:\Users\joach\OneDrive - EDUETATFR\Documents\Moi\crypto-trade-journal\.venv\Lib\site-packages\PyInstaller\building\icon.py", line 54, in normalize_icon_type
    raise ValueError(
    ...<4 lines>...
    )
ValueError: Received icon image 'C:\Users\joach\OneDrive - EDUETATFR\Documents\Moi\crypto-trade-journal\bybit_journal\frontend\asset\icon.ico' which exists but is not in the correct format. On this platform, only ('exe', 'ico') images may be used as icons. If Pillow is installed, automatic conversion will be attempted. Please install Pillow or convert your 'ico' file to one of ('exe', 'ico') and try again.
(.venv) PS C:\Users\joach\OneDrive - EDUETATFR\Documents\Moi\crypto-trade-journal\bybit_journal\desktop>