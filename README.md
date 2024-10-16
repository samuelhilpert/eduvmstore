# EduVMStore

## Projektübersicht

Dieses Projekt umfasst die Entwicklung eines **AppStores** zur Bereitstellung von Anwendungen auf einer OpenStack-Plattform. Das Ziel ist es, Dozenten die Möglichkeit zu geben, Anwendungen zu deployen, die von Studierenden im Rahmen von Lehrveranstaltungen genutzt werden können, ohne tiefere Kenntnisse in OpenStack zu benötigen. Der Fokus liegt auf automatisierter Konfiguration und einfacher Verwaltung.

### Hauptfunktionen
- **Automatisiertes Deployment**: Vereinfachter Bereitstellungsprozess mit automatisierten Schritten für die Konfiguration von VMs, Benutzerkonten, Netzwerkeinstellungen usw.
- **Unterstützung verschiedener Anwendungen**: Der AppStore kann vorgefertigte Umgebungen bereitstellen

Dieses Projekt wird im Rahmen des Moduls "Projekt" an der DHBW Mannheim im Zeitraum von August 2024 bis Mai 2025 umgesetzt.

## Projekt-DEV-Setup und Run
### Datenbank lokal
* ``python eduvmstorebackend/manage.py makemigrations``
* ODER ``python3 eduvmstorebackend/manage.py makemigrations``
* ``python3 eduvmstorebackend/manage.py migrate ``
* ODER ``python eduvmstorebackend/manage.py migrate ``
* `db.sqlite3` Datei doppelklicken
* Im Pop-Up unten auf "Download missing Drivers" gehen und Installation abwarten und auf "OK" gehen

### Backend Server lokal starten:
* ``python3 eduvmstorebackend/manage.py runserver localhost:8000
``
* Zugang über localhost:8000

### API-Zugriff
* Zugriff über ```localhost:8000/api/<endpoint>```
* ``<endpoint>``: Z.b. ``<base-url>/app-templates/...``, ``<base-url>/users/...``