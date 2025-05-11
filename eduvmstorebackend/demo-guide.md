# EduVMStore Demo Anleitung

## Vorbereitungsschritte vorher treffen
- **Zugriff auf die Demo-OpenStack-Umgebung prüfen**
  - http://141.72.13.84
  
- **Ungewollte AppTemplates und Instanzen löschen**
  - Instanz und AppTemplates, die in vergangenen Demos erstellt wurden, löschen.

- **Sicherstellen, dass ein Image oder Snapshot "EM-Pentesting-ITSEC" vorhanden ist**
  - ggfs. normaler OpenStack Prozess erstellen

---

## Einführung / Begrüßung
- **Herzlich willkommen zur Demo des EduVMStores**
  - Ziel: Ermöglichen von Dozierenden der DHBW das Teilen und Wiederverwenden von (erweiterten) VM-Vorlagen.
  - Fokus: Vereinfachung des VM-Aufsetzens, besonders für weniger technisch versierte Dozierende.

---

## Vorgehen

1. **Anmeldung in OpenStack**
   - Anmeldung mit Benutzername: `admin` und Passwort: `nomoresecret`.
   - Nutzung des integrierten Plugins, keine separate URL oder Passwort erforderlich.

2. **Navigieren zum EduVMStore**
   - Links in der OpenStack-Navigationsleiste den Reiter „EduVMStore“ auswählen.
   - Auf „Dashboard“ klicken, um die Übersicht der bestehenden App-Templates zu sehen.

3. **Übersicht der App-Templates**
   - Alle verfügbaren App-Templates werden mit wichtigen Informationen angezeigt.
   - Ein AppTemplate ist ein Wrapper für ein VM-Image, der zusätzliche Funktionalität zur Instanziierung bereitstellt.

4. **Detailansicht eines App-Templates**
   - Klick auf den Namen eines App-Templates, um die Detailansicht zu öffnen.
   - Informationen zu diesem Template werden angezeigt.

5. **Erstellen eines neuen App-Templates**
   - Zurück zum Dashboard und „Create AppTemplate“ klicken.
   - Auswahl eines bestehenden Images (z.B. „EM-Pentesting-ITSEC“) als Grundlage.
   - Felder wie Name, Beschreibung und Hinweise zur Instanziierung ausfüllen.
   - Sichtbarkeit als „Public“ oder „Private“ festlegen.
   - Benötigte Ressourcen (z.B. CPU, RAM) je nach Nutzeranzahl anpassen.
   
6. **Erweiterte Funktionen (optional)**
   - Möglichkeit, ein Skript hochzuladen oder direkt zu schreiben (z.B. für Nutzeranlegung in GitLab oder der VM).
   
7. **App-Template erstellen**
   - Auf „Create“ klicken, um das neue App-Template zu speichern.
   - Das neue App-Template erscheint in der Übersicht.

8. **App-Template instanziieren**
   - Mit „Launch-Instance“ kann das Template zu einer Instanz werden.
   - Später: CSV-Dateien mit Benutzerdaten und Passwörtern hochladen.
   - Instanzgröße (Flavor) und Name auswählen. Diese Felder sind später automatisch vorausgefüllt.

9. **Überprüfung in OpenStack**
   - Nach dem Klick auf „Launch“ ist die Instanz in OpenStack erzeugt.

10. **Weitere Funktionen**
    - In der linken Navigationsleiste gibt es ein Tutorial für den EduVMStore.
    - Die Admin-Seite dient zur Verwaltung weiterer Administratoren.

---

## Abschluss-Fragen
- **Was halten Sie von der Lösung?**
- **Welche Probleme sehen Sie?**
- **Was würden Sie sich noch wünschen?**
