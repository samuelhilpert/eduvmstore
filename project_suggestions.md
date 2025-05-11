### Project Suggestions/Projekterweiterungen
In this file, all thoughts and ideas about future development of the project is listed.

Beware that the suggestions are in German as the developers are German and those ideas will probably be better understood in German. The order does not convey any meaning or importance.

### Ideas listed
1. Instanzen verlinken und gemeinsam mit AppTemplate löschen (bereits erster Ansatz für Backend auf dem Branch instance-link in dem eduvmstore Repo)
2. Manuellen Installationsschritt aus Kola-Ansible Installation lösen
3. Noch mehr Beispiele aus der Praxis 
3. Security Groups automatisch bei der Instanziierung erstellen (besonders für die BeispielappTemplates sinnvoll)
4. Tooltips auch für die variablen Felder 
5. Ausprobieren von noch nativeren Openstack Angular Integration (siehe auch [search-engine-horizon-experiment](https://github.com/samuelhilpert/eduvmstore-ui/compare/dev...search-engine-horizon-experiment) Branch im Frontend Repo)
6. Nutzerfeedback und Probleme aus der Produktivschaltung 
7. Verbindung mit dem DHBW-Rollenmanagement für das automatische Anlegen eines Kurses  (z.B. nur noch auswählen WWI22SEA mit automatische PW-Generierung statt CSV-Datei mit allen Studenten)
8. Gegebenenfalls für einfacheren Betrieb/Geringere Fehlertoleranz: Verschieben der Backendlogik in das Horizon Plugin (dann sind keine API-Calls mehr notwendig, eine strenge Separierung findet sowieso nicht statt, da das Frontend auch Logik (wie Instanziierung durch die engere Integration mit Openstack durchführt)
9. LLM-Integration zum einfacheren Schreiben/Bearbeiten von Skripten. 
10. Unterstützung für die korrekte Einrückung und Fehlererkennung/Fehlerbehebungsvorschlag 
11. Drag & Drop für CSV-Upload 
12. Tutorial als PDF-Version downloadbar 
13. Sicherstellen, dass Eingaben bestehen bleiben, wenn die Anzahl der Eingabeentitäten verändert wird (Beispiel: ich instanziiere ursprünglich 2 AppTemplates und verändere beim ersten die Security Group, wenn ich jetzt stattdessen 3 oder 1 auswähle, sollte die Security group bei dieser Instanz erhalten bleiben. Gleiches gilt für die Benutzerentitäten.)
14. Überprüfung der Verwendung von Short Description —>ggfs löschen 
15. Suchfunktion fehlertolerant machen 
16. Inklusion mehrerer VMs in einem AppTemplate: Beispiel Datenbank und Backend in zwei unterschiedlichen VMs zusammen (aufeinander abgestimmt) instanziierbar 
17. Ablaufdatum für Instanzen —>Danach automatisch gelöscht 
18. Inkludieren von RessourcenManagement —>Möglichkeit, Flavours automatisch auf Basis der Konfigurationen in der Instanziierung erstellen lassen
19. Implementation unabhängiger vom Betriebssystem der VM machen, um z.B. Windows VMs zu unterstützen
20. Mehr Reporting und Analysemöglichkeiten zum besseren Verständnis der Nutzung des EduVMStores (z.B. welche AppTemplates sind am beliebtesten, zu welchen Zeiten werden AppTemplates erstellt ...)
