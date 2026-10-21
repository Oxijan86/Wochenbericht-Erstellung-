# Wochenbericht Lovrencic – V2.9.0

GitHub-Pages-fähige, offline nutzbare Wochenbericht-Anwendung für Servicetechniker. Die Anwendung speichert Daten lokal im Browser (IndexedDB) und kann mit freigegebenen lokalen beziehungsweise synchronisierten Ordnerdateien arbeiten, sofern der Browser dies unterstützt. Exportierte Datenbank: `wochenberichte.db`.

## Neue Funktionen in 2.9.0

1. **Reisezeit und Pause einfacher eingeben:** `130` oder `0130` werden zu `1:30`, `030` zu `0:30`; der Doppelpunkt wird automatisch ergänzt. Bestehende Schreibweisen wie `1:30` und `1,5` sind weiterhin erlaubt. Aufrundung auf Viertelstunden.
2. **Optionale Pause:** Wahlweise von Arbeitszeit oder Reisezeit abziehen; Nettozeiten erscheinen in der Erfassung, in Übersichten und beim Export.
3. **Arbeit über Mitternacht:** Tatsächliches Enddatum festhalten; eine frühere Enduhrzeit ohne Enddatum bedeutet Folgetag. Die Zeitspanne wird geprüft.
4. **Laufende Einsätze:** Nach „Beginn ab jetzt“ und Bestätigung auch ohne Endzeit speichern; im Dashboard aufrufen und beenden.
5. **Montag bis Sonntag und mehr als sechs Einsätze pro Tag:** Sämtliche Einträge werden in Historie und Datenbank geführt. Das **unveränderte Excel-Original** kann maximal sechs Einträge je Montag–Freitag zeigen. Bei Überlauf beziehungsweise Wochenenden exportiert die Anwendung zusätzlich eine vollständige TSV-Wochenübersicht mit allen Einträgen.
6. **Exportprüfung:** Prüft vor dem Excel-Export unter anderem offene Einsätze, fehlende Arbeitsdauer, ungültige Zeitspannen und Pausen, mögliche Dubletten, Überschneidungen sowie nicht darstellbare Einträge.
7. **M365-Fehlerkarten:** Ungültige Importzeilen – etwa ohne Einsatzdatum oder mit fehlenden Spalten – werden mit Zeilennummer und Begründung angezeigt und dürfen korrigiert oder ausdrücklich ausgelassen werden. Solange eine fehlerhafte Zeile unbearbeitet bleibt, ist der gemeinsame Import gesperrt.
8. **Vollständig aktualisierter Hilfe-Reiter:** Acht Themenbereiche, passende Sprungschaltflächen, aktuelle Versions- und Exporthinweise.

## Einstieg

- **Neue Installation:** `index.html` öffnen beziehungsweise die GitHub-Pages-URL besuchen und im Einrichtungsassistenten „Neue Datenbank erstellen“ wählen.
- **Vorhandene Daten:** Bisherigen Browserdatenbestand weiterverwenden oder die gesicherte `wochenberichte.db` importieren. Vor einem Versionswechsel immer eine Datenbanksicherung erstellen.
- **M365:** Beliebig viele Serviceberichte gemeinsam in Copilot auswerten. Pro Einsatz eine TAB-getrennte Zeile mit **neun Feldern** zurückgeben lassen. `M365 & Datenimport` → Ergebnis einfügen → `Daten prüfen` → Fehler beheben bzw. ausdrücklich ausschließen → individuelle Übernahmevorschau prüfen → `Auswahl bestätigen und speichern`. Die ausgewählte Bildschirm-KW beschränkt den Import nicht; das Einsatzdatum bestimmt die Ziel-KW.
- **Excel:** Im Export-Reiter die Datenprüfung lesen. Wenn es Zusatz-Einsätze gibt, gehören XLSX und ergänzende TSV-Datei zusammen; die Originalvorlage bleibt unverändert.
- **Schließen:** Über Schaltfläche im Kopfbereich beziehungsweise Hamburger-Menü „Speichern / Synchronisieren / Schließen“. Lokales Speichern funktioniert auch ohne Ordnerfreigabe.

## GitHub Pages

In einem öffentlichen Repository `index.html`, `sw.js`, `README.md` und `.nojekyll` im Root-Verzeichnis ablegen. Unter `Settings → Pages` die Branch `main`, Ordner `/ (root)` veröffentlichen. Vorhandene Dateien beim Versionswechsel ersetzen. Der Service-Worker-Cache wurde auf `wochenberichte-static-v2.9.0` erhöht.

**Datenschutz:** Niemals eine persönliche `wochenberichte.db`, Serviceberichte oder eigene Kundenlisten nach GitHub hochladen. Das ausgelieferte Repository enthält eine anonymisierte Vorlage und keine konkreten Kundendaten.

## Technische Grenzen

- Eine reine Browserinstallation auf Android kann keine automatische Synchronisierung mit OneDrive/Google Drive garantieren. Ohne unterstützte dauerhafte Ordnerfreigabe Datenbankexport und -import verwenden.
- Synchronisationsordner besitzen keine atomare Mehrgeräte-Sperre. Für gleichzeitige Bearbeitungen auf verschiedenen Geräten wäre eine serverseitige Lösung erforderlich.
- Die Original-Excel-Datei ist eine feste Vorlage für Montag bis Freitag mit sechs Einsatzzeilen pro Tag. Diese Begrenzung wird nicht verdeckt; die vollständige TSV-Zusatzübersicht ist für darüber hinausgehende Einsätze notwendig.
- Interne Browser-Simulationen ersetzen keinen Praxistest auf einem physischen Smartphone mit realem Cloud-Ordner.
