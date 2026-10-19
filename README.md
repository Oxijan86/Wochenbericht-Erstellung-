# Wochenbericht Lovrencic – Web-Anwendung V2.4

Offlinefähige Wochenbericht-Erstellung im Original-Excel-Format mit SQLite-Datei, IndexedDB, revisionsgeschützter Ordnersynchronisierung und Backups. **Kein Backend, kein Account und keine Installation notwendig.** Die öffentliche Projektfassung enthält anonymisierte Musterdaten und eine bereinigte Excel-Layoutvorlage; die Vorlage behält die ursprünglichen Spalten, Zellformatierungen, Druckeinstellungen und Tabellenstruktur.

## Sofort starten

1. `index.html` in Chrome oder Edge öffnen. Alternativ die Anwendung über GitHub Pages bereitstellen.
2. Beim ersten Start **Neue Datenbank erstellen** wählen, Technikername und Personalnummer eingeben. Alternativ **Vorhandene Datenbank öffnen** wählen und eine geprüfte `wochenberichte.db` importieren.
3. Auf dem **Dashboard** die aktuelle KW, Tages-/Wochenstunden, Freizeitausgleich und die letzten 20 erfassten Einsätze ansehen. Unter **Einsätze erfassen** Einsätze, Homeoffice ohne Ticket, Reise- und Arbeitszeiten erfassen. Für Serviceberichte unter **M365 & Datenimport** den RONDO-Prompt kopieren und TAB-getrennte Ergebnisse importieren.
4. Unter **Wochenbericht / Export** eine Excel-Datei im Originalformat herunterladen. Die Datei wird mit dem offiziellen Excel-MIME-Typ ausgegeben; auf Android in Microsoft Excel über **Öffnen → Dieses Gerät → Downloads** öffnen.
5. Unter **Speicherung & Sync** den Modus einstellen. Unter **Backups** Sicherungen prüfen und exportieren.


## Neue Oberfläche V2.4

- **Dashboard als Startseite:** Zeigt den ausgewählten Techniker, die aktuelle ISO-Kalenderwoche, die an diesem Kalendertag gebuchten Gesamtstunden (Arbeit + Reise), die Wochenstunden, die Differenz zum vollständigen Wochen-Soll und den Freizeitausgleich-Saldo. Noch nicht erreichte Wochen-Sollstunden werden auch während einer laufenden Woche angezeigt; es handelt sich **nicht** um eine Tages-Sollberechnung.
- **20 zuletzt hinzugefügte Einträge:** Die Sortierung basiert bei neuen Einträgen auf `createdAt` (Erfassungszeitpunkt), **nicht** auf dem Einsatzdatum. Beim Bearbeiten bleibt der ursprüngliche Erfassungszeitpunkt erhalten. Für frühere Einträge ohne `createdAt` wird ein Zeitstempel aus der älteren Datensatz-ID verwendet, soweit vorhanden, sonst das Einsatzdatum. Alte Einträge werden dafür nicht verändert. Einträge stammen aus allen Kalenderwochen des **aktiven Technikers**.
- **Aktionen im Dashboard:** „Bearbeiten“ öffnet die betreffende ursprüngliche Woche. „Übernehmen“ kopiert den Einsatz in ein neues Formular, ohne Datum oder Arbeitszeiten zu übernehmen.
- **Smartphone-Navigation:** Bis 780 Pixel Bildschirmbreite ersetzt das ☰-Menü die Reiter. Es schließt nach der Auswahl automatisch. Auf dem Desktop bleiben die Reiter bestehen.
- **Einsatzdaten:** Standardmäßig werden alle Monate durchsucht; die bisherige Zusatz-Checkbox entfällt. Filter sind optional für Monat, Jahr, individuelles Datumsintervall, Kunde, Ort und Tätigkeitsart. Unter „Weitere Filter & Sortierung“ werden selten benötigte Einstellungen ausgeblendet.
- **Kundenübernahme:** Beim Schreiben eines Kundennamens erscheinen ältere Einsätze zur Auswahl, nach Kundenstandort und optionaler Kundennummer unterschieden. Nach der Auswahl ausdrücklich **Vorhandene Kundendaten übernehmen** verwenden. Die gemeinsame Vorschau lässt Kilometer und Reisezeit zunächst eingeschaltet. Ticket, Bemerkungen, alte Tätigkeiten und Arbeitszeiten werden immer geleert. Das neue Datum bleibt erhalten.
- **Tageszeile:** Oberhalb der Zeiterfassung werden die Gesamtstunden des ausgewählten Tages und die ausgewählte KW angezeigt.
- **Speicherstatus:** Im Dashboard steht ein kompakter aktueller Status; Berechtigungen, Konflikte und Backups bleiben in den bisherigen Verwaltungsbereichen.

### Übergang von V2.2

Das SQLite-App-State-Schema, die Datenbankidentität, die bisherigen Revisionsmetadaten sowie das Excel-Originalformat bleiben erhalten. `createdAt` ist ein **optionales neues Feld einzelner Einsatzdatensätze**, das nur bei neu angelegten Einträgen geschrieben wird. Bestehende Einträge ohne das Feld bleiben unverändert. Vor dem Wechsel die aktuelle `wochenberichte.db` herunterladen. Browserdaten werden durch ein HTML-Datei-Update auf einer **neuen URL bzw. Origin** nicht automatisch übertragen.

## GitHub Pages veröffentlichen

1. Neues Repository anlegen, Dateien aus diesem Paket **ins Stammverzeichnis** hochladen (`index.html` und `sw.js` müssen nebeneinander liegen).
2. Unter **Settings → Pages** die Veröffentlichung aus dem Hauptbranch und `/ (root)` aktivieren.
3. Die angezeigte HTTPS-Adresse öffnen. Beim ersten Online-Aufruf speichert der Service Worker die Anwendungsdatei für spätere Offline-Aufrufe zwischen. **Dieser Cache ist keine Datensicherung.**
4. Benutzer legen je Browser/Browserprofil ihre eigene Datenbank an. Der öffentliche Repository-Inhalt enthält **keine privat gespeicherten Einsatzdaten**.

Wichtig: Daten in IndexedDB sind an die **konkrete Website-Adresse, den Browser und das Benutzerprofil** gebunden. Beim Umzug zu einer anderen URL vorher unbedingt `wochenberichte.db` herunterladen und dort importieren. Auf einem Smartphone ohne Ordnerfreigabe ist diese Methode der Geräteübertragung vorgesehen.

## Speicherarten

| Modus | Verhalten |
|---|---|
| Nur auf diesem Gerät | Dauerhafte lokale SQLite-Arbeitskopie in IndexedDB; separater `.db`-Download und Import |
| Lokaler Ordner | Ordnerzugriff des Browsers nach Freigabe; `wochenberichte.db` wird ca. 250 ms nach erfolgreichem lokalen Speichern abgeglichen |
| Cloud-Synchronisationsordner | Wie lokaler Ordner, aber Benutzer wählt einen **lokal** von z. B. OneDrive synchronisierten Ordner. Der Dienst synchronisiert zwischen Computern. |

Die Ordnerfunktion setzt **HTTPS bzw. eine unterstützte sichere Umgebung** und einen kompatiblen Browser mit File System Access API (`showDirectoryPicker`) voraus. Sie funktioniert nicht in allen mobilen Browsern. Browser-only bleibt immer verfügbar. Eine importierte Datei ist **keine** automatische Ordnerfreigabe.

### Richtig zwischen Geräten wechseln

1. Auf Gerät A die Änderungen lokal speichern und **Jetzt synchronisieren** wählen. Auf fehlerfreien Abschluss warten.
2. Synchronisierungsdienst des Betriebssystems (z. B. OneDrive) auf die aktuelle Datei abgleichen lassen.
3. Auf Gerät B denselben synchronisierten Ordner öffnen und **Vorhandenen Dateistand laden** auswählen. Nicht unabhängig auf beiden Geräten denselben Ausgangsstand ändern.
4. Ohne Ordnerzugriff: auf A `wochenberichte.db` herunterladen, per Dateiübertragung nach B bringen, auf B als Datenbank öffnen/importieren.

Ein Ordnerdienst bietet **keine atomare Sperre oder transaktionale Versionsprüfung über mehrere Geräte**. Zwei absolut gleichzeitige Schreibvorgänge können weiterhin kollidieren. Ein zentraler Server ist für garantiert gleichzeitige Mehrbenutzerbearbeitung erforderlich. Unabhängig geänderte Kopien werden nicht automatisch zusammengeführt.

## Backup & Wiederherstellen

- Vollständige lokale Backups nach ca. 15 Sekunden Ruhe, beim Start (falls 24 h überschritten), vor ersetzenden Operationen und beim geordneten Schließen.
- Im verbundenen Ordner nach Freigabe zusätzlich im Unterordner `Backup` (sofern Zugriff möglich).
- Je Ablage werden die letzten 30 anwendungseigenen Sicherungen aufbewahrt; fremde Dateien werden nicht gelöscht.
- Vor einer Wiederherstellung den Datensatz, enthaltene Einsatzanzahl und Revision prüfen. Danach bleibt der wiederhergestellte Stand **lokal und unveröffentlicht**, bis die Veröffentlichung ausdrücklich bestätigt wird.
- Automatische Backups laufen **nur, während die Seite geöffnet ist**.

## Technische Architektur

- **Eine SQLite-3-Datei** `wochenberichte.db` mit einer Tabelle `app_state(payload TEXT NOT NULL)`, in der der vollständige Anwendungszustand als JSON einschließlich der Revisionsmetadaten enthalten ist. Diese Datei wurde mit dem regulären SQLite-Prüfkommando `PRAGMA quick_check` verifiziert. Das im Paket enthaltene JavaScript-Codec-Modul erzeugt und liest dieses fest definierte SQLite-Format eigenständig; es ist **kein allgemeiner SQL.js-Abfrageadapter**. Fremde SQLite-Schemas werden aus Sicherheitsgründen abgewiesen.
- Browser-Arbeitskopie sowie lokale Sicherungen über IndexedDB, asynchrone Transaktionen mit dauerhafter Bestätigung.
- `database_id`, monoton steigende `revision`, neue `revision_id`, `previous_revision_id` und zuletzt bestätigte gemeinsame Basis.
- Zentrale Warteschlange für automatische und manuelle Syncs und die Abschluss-Synchronisierung; Lesen und Revisionsprüfung vor Schreiben, Dateiprüfung nach Abschluss.
- Nach gespeicherten Änderungen erstellt die Anwendung auf Wunsch zusätzlich wiederherstellbare Backup-Dateien im Ordner.
- Keine Datenübertragung an einen fremden Webserver durch diese Anwendung.

## Migration von V1.3

Wenn die alte Browser-`localStorage`-Ablage aus derselben Browserumgebung erreichbar ist, wird sie geprüft, zunächst als JSON-Originalsicherung abgelegt und anschließend zur neuen SQLite-Arbeitskopie migriert. Die Originaldaten werden erst nach erfolgreicher Migration aus dem alten Key entfernt. Andernfalls: **zuerst in V1.3 eine JSON-Sicherung exportieren**, danach in V2.0 **Alte JSON-Daten importieren**. Bei einem Wechsel auf GitHub Pages ist dieser manuelle Weg häufig erforderlich, da Dateiseite und Website unterschiedliche Speicherbereiche besitzen.

## Datenschutz und Lizenz

Dieses GitHub-Paket verwendet anonymisierte Beispieldaten und eine bereinigte Druckvorlage. **Bitte keine persönlichen `.db`-Dateien, Backups oder Serviceberichte in öffentliche GitHub-Repositories hochladen.** Die Anwendungslogik ist unter MIT veröffentlicht; die eingebettete JSZip-Bibliothek unter ihrer eigenen MIT/GPL-Lizenz (siehe `THIRD_PARTY_NOTICES.md`).

## Projektdateien

- `index.html` – unmittelbar lauffähige Anwendung; enthält alle JS-Bibliotheken und die Vorlage (kein CDN nötig)
- `sw.js` – statischer Offline-Cache für GitHub Pages
- `src/` – Quellmodule, HTML-Basis und Anwendungskern
- `vendor/jszip_script.html` – eingebundene JSZip-Bibliothek mit Drittanbieterhinweisen
- `tools/build.py` – generiert `index.html` nach Änderungen in `src/`: `python tools/build.py`
- `tests/` – Python/Playwright-Browsertests und Testadapter (Simulation, nicht echte Geräte)
- `TESTPROTOKOLL.md` – Umfang und Grenzen der durchgeführten Tests

**Bekannte Grenze:** Die Anwendung bietet einen echten SQLite-Dateicontainer, aber keine relationale Mehrtabellenstruktur wie die Lagerverwaltung. Eine Umstellung auf SQL.js mit normalisierten Tabellen ist ein möglicher späterer Architektur-Schritt.

## Ergänzungen V2.2

- Ticketnummern sind **bei allen Tätigkeitsarten optional**, auch bei Kundeneinsätzen und beim M365-Import. Die neun TAB-Spalten bleiben unverändert; ein leeres Ticket-Feld zwischen TABs ist zulässig.
- Technikerprofile werden über ein eigenes Formular angelegt und bearbeitet (Name, Personalnummer, Sollstunden, Anfangssaldo).
- **Profil löschen:** Ein leeres Profil wird nach Sicherheitsbackup gelöscht. Ein Profil mit zugehörigen Wochenberichten wird sicher archiviert und aus der Auswahl genommen, ohne Berichte zu löschen. Über **Archivierte Technikerprofile** lässt es sich wiederherstellen. Eine endgültige Löschung mit Einsätzen erfordert gesonderte Bestätigung und exakte Eingabe des Namens; zuvor wird die vollständige Datenbank gesichert. Das letzte aktive Profil bleibt geschützt.
- SQLite-Datenstruktur und Exportformat sind unverändert kompatibel mit V2.0.

## Excel-App unter Android / V2.2

Version 2.2 korrigiert den XLSX-Download: offizieller MIME-Typ `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`, 60 Sekunden URL-Lebensdauer, ursprüngliches Drucklayout weiterhin unverändert. Die eingebettete Vorlage enthält keine private OneDrive-Pfadreferenz mehr.

Auf Android: im Browser **Wochenbericht / Export → Excel (.xlsx) exportieren** verwenden. Datei im Download-Ordner speichern; Excel öffnen und über **Datei öffnen** die `.xlsx` auswählen. Nicht `.db`, `.json` oder `.tsv` auswählen. Falls eine vorhandene heruntergeladene Datei defekt erscheint, mit V2.2 neu exportieren.

Auch eine technisch valide XLSX-Datei kann je nach Excel-App-Version und Android-Dateianbieter gesonderte Probleme verursachen; für einen solchen Fall die Fehlermeldung und einen anonymisierten Export zur Analyse bereitstellen.


## Neu in V2.4 – geführte Einrichtung und Übernahme

### Einrichtungsassistent

1. **Neue Datenbank erstellen** nur für einen neuen Datenbestand auf Gerät A wählen oder **Vorhandene Datenbank öffnen** für ein zweites Gerät mit einer bereits exportierten `wochenberichte.db`. Die Datei wird vor dem Import auf Format und Datenintegrität geprüft.
2. **Lokal auf diesem Gerät** oder **Über Cloud-Synchronisationsordner** auswählen. Auch bei Cloud-Wunsch existiert zunächst eine echte lokal gespeicherte Browser-Arbeitskopie.
3. Bei Browsern mit File System Access API kann optional über **Speicherordner auswählen** ein Ordner verbunden werden. Ohne Picker (häufig auf Android) ist **keine automatische Ordnersynchronisierung** möglich. Die Einrichtung bleibt nutzbar; Austausch über Datei herunterladen/importieren.
4. Vor dem Abschluss die Zusammenfassung prüfen; **Einrichtung abschließen und Anwendung starten** speichert lokal dauerhaft. Speicheroptionen später unter **Speicherung & Sync** ändern. Bestehende Ordnerdateien werden bei Verbindung nicht still überschrieben.

**Google Drive / OneDrive:** Es existiert **keine direkte Cloud-API-Anmeldung**. Ein tatsächlich für den Browser nutzbarer und vom Cloud-Anbieter synchronisierter lokaler Ordner ist Voraussetzung. Die Installation der Smartphone-App allein genügt nicht. Unternehmenskonten können Sicherheitseinschränkungen haben. Vor dem Gerätewechsel: Gerät A speichern/synchronisieren, Gerät B laden; niemals auf B unabhängig eine neue Datenbank für denselben Bestand anlegen.

### Frühere Einsätze und Kundendaten

- Übernahme aus dem Reiter **Einsatzdaten**, dem **Dashboard** sowie über **Kundenvorschläge** verwendet dieselbe Vorschau.
- **Kunde, Einsatzort und vorhandene Stammdaten** (Kundennummer, Anschrift, PLZ/Ort, Filiale) werden übernommen. **Kilometer und Reisezeit** sind standardmäßig angehakt und können unabhängig abgewählt werden. **Ticketnummer, Bemerkung, Arbeitsbeginn/Ende, Arbeitsdauer und Tätigkeit** werden nicht aus dem alten Einsatz übernommen. Das neue ausgewählte Datum bleibt erhalten.
- Neue Kundenstammdaten lassen sich im manuellen Formular über **Weitere Kundenstammdaten (optional)** hinterlegen und bleiben im SQLite-Datenbankinhalt. Das Original-Excel-Drucklayout wird nicht verändert.
- Die Vorschläge ignorieren Groß-/Kleinschreibung, akzentbedingte Unterschiede und überzählige Leerzeichen, unterscheiden aber gleiche Namen an verschiedenen Standorten. **Auch ältere Treffer desselben Standorts** sind auswählbar.
- Eine Vorschau allein legt **keinen** neuen Eintrag an. Gespeichert wird erst über **Eintrag speichern**. Auch bisherige gespeicherte Einträge bleiben unangetastet.

### V2.3 → V2.4

Die Datenbankstruktur und der Original-Excel-Export bleiben kompatibel. Vor dem Wechsel trotzdem `wochenberichte.db` sichern. Läuft die neue GitHub-Pages-Version unter derselben URL und demselben Browserprofil, bleibt die IndexedDB-Arbeitskopie erreichbar. Eine lokal geöffnete HTML-Datei oder eine andere Domain/URL kann einen **anderen** Browser-Speicherbereich verwenden; dort die exportierte `.db` importieren.
