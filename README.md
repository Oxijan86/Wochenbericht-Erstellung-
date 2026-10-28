# Wochenbericht Lovrencic – V2.24.1 (28.10.2026)

Browser-Anwendung für PC und Smartphone mit lokal gespeicherter SQLite-kompatibler Datenbank (`wochenberichte.db`), IndexedDB und optionaler Ordnersynchronisation. **Bitte vor jedem Update eine separate Sicherung der produktiven Datenbank anlegen.**

## V2.24.1 – Korrekturen

- **Kundenauswahl im Einsatzassistenten:** statt Dropdown ein durchsuchbares Eingabefeld; Tippvorschläge nach Name, Kundennummer, Standort und Adresse; jede Filiale einzeln wählbar. Nach Auswahl übernimmt der Assistent den Kunden und seine vorhandenen Adressdaten. Neue Kunden/Standorte bleiben möglich.
- **Uhrzeitkorrektur:** über „Alle Uhrzeiten korrigieren“ auf alle bereits erfassten Zeitstempel zugreifen. Hinfahrt, Ankunft, Arbeit und Rückfahrt werden mit Datumsangaben bearbeitet; über Mitternacht möglich. Gemessene Fahrzeiten und Nettoarbeitszeit werden neu berechnet; vorhandene Fahrt-/Arbeitspausen berücksichtigt. Bei unmöglicher Zeitfolge wird nichts gespeichert. Bei Kundenwechsel erfolgt die Aufteilung der bestätigten Gesamtfahrt wiederholbar ohne Doppelzählung.
- **PDF-Gesamtabgleich bei mehrtägigen Einsätzen:** Jetzt **beim PDF-Direktimport** aufgerufen. Das PDF-Datum zählt als letzter Einsatztag; zusammengehörige Tagesbuchungen (gleiches Ticket und passender Kundenstandort, maximal 14 Tage zurück) werden addiert und mit PDF-Gesamtsummen verglichen. Ausdrückliche Entscheidung erforderlich. Kein Überschreiben der Tageswerte; alle beteiligten Tage werden mit PDF-Prüfnachweis gekennzeichnet. Eintägige PDF-Berichte werden weiterhin wie bisher verarbeitet.
- **PDF-Prüfkennzeichnung bleibt nach einer Uhrzeitkorrektur bestehen.** Änderungen können im vorhandenen Prüfnachweis als Nachbearbeitung dokumentiert sein, ohne eine neue Prüfung zu erzwingen.
- **Version und Offline-Cache:** V2.24.1, Netz-zuletzt-Cache nur für die statische Anwendung; alte Cache-Versionen beim Aktivieren entfernt. IndexedDB und externe `.db`-Dateien werden nicht gelöscht.

## Vorherige Funktionen (bleiben erhalten)

- PDF pro Datei übernehmen oder vollständig überspringen, Technikerpositionen kontrollieren, ausdrückliche Übernahme.
- Manuelle Dienstreise-, Arbeits- und Pausenerfassung; Einsatz abbrechen; nächster Kundenstandort, Fahrzeitvorschläge, letzter Kilometerstand.
- Historische Excel-/M365-Importe mit Dublettenprüfung und Kundenstamm; Exportprüfung, Kalenderwochen und Exportvorlage.
- Mehrere Techniker optional, Kundendatenverwaltung, gespeicherte Einsätze und Historie, SQLite-Datenaustausch, Sync/Backups.

## GitHub Pages und Update

Den **gesamten Inhalt des ZIP** im Root von `Oxijan86/Wochenbericht-Erstellung-` hochladen. Mindestens `index.html` und `sw.js` gemeinsam ersetzen; zusätzliche Dokumentations- und Testdateien können ebenfalls überschrieben werden. `.nojekyll` unverändert belassen. Auf Android bzw. am PC nach dem Deployment neu laden (bei installiertem Offline-App-Icon ggf. App schließen und erneut öffnen). Die neue App zeigt **Version 2.24.1** an.

**Niemals** Browser-Sitedaten bzw. IndexedDB löschen, um einen veralteten Offline-Cache zu bereinigen. Vorher separate `wochenberichte.db`-Datei sichern. Bestehende Datenbankstruktur wird durch dieses Update nicht migriert.

## Testgrenzen

Automatisierte Chromium-Tests mit PC- und mobilem Viewport sind keine Prüfung auf einem realen Android-Gerät. Produktive OneDrive-Synchronisation, echte RONDO-PDFs und die produktive Datenbank wurden aus Datenschutz- und Zugriffsgründen nicht getestet. Details und Reproduktionsmöglichkeiten in `TESTPROTOKOLL.md`.
