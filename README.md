V2.24.5 (28.10.2026): Mehrtägige PDF-Zuordnung auch ohne vorhandene Ticketnummer, gleiche Kunden und kompatible Standorte innerhalb von 28 Tagen, explizite Tagesauswahl, Summenvergleich ohne Überschreiben.


## V2.24.3: automatische Stempel und Korrekturen
Beim Kunden angekommen beendet die Hinreise und startet die Arbeitszeit. Im Assistenten „Stempelzeiten bearbeiten“ sind alle bisher erfassten Zeiten und Pausen einschließlich Datum sichtbar. Neue Pausen können ergänzt, vorhandene korrigiert oder durch Leeren beider Datumsfelder entfernt werden. Der Schalter „Auto-Start: Ankunft = Arbeitsbeginn“ ist standardmäßig aktiv. Der zweite Schalter verknüpft Arbeitsende und Rückfahrtbeginn, sofern eine Rückfahrt erfasst bzw. bewusst gestartet wird. Die Rückfahrt selbst startet nicht von allein. Beide Schalter lassen sich pro Einsatz deaktivieren. Alle Anpassungen erst nach „Korrekturen speichern“ übernehmen. Die 28-Tage-PDF-Suche aus V2.24.2 bleibt erhalten.

# Wochenbericht Lovrencic – V2.24.2 (28.10.2026)

Browser-Anwendung für PC und Smartphone mit lokal gespeicherter SQLite-kompatibler Datenbank (`wochenberichte.db`), IndexedDB und optionaler Ordnersynchronisation. **Bitte vor jedem Update eine separate Sicherung der produktiven Datenbank anlegen.**

## V2.24.2 – PDF-Gesamtabgleich über vier Wochen

- **28-Tage-Suche:** Beim direkten PDF-Import werden weitere Einsatztage desselben Kunden und Standorts bis zu 28 Tage rückwärts ab dem PDF-Enddatum vorgeschlagen. Vorhandene gleiche Ticketnummern werden erkannt; **fehlende** Ticketnummern verhindern keinen Vorschlag mehr. Abweichende vorhandene Ticketnummern werden ausgeschlossen.
- **Tage ausdrücklich auswählen:** Alle möglichen Tage erscheinen mit Datum, Kunde, Standort, Ticket und Kilometern als Auswahlkästchen. Eindeutig gleiche Tickets sind vorausgewählt; Tage ohne Ticket sind **nicht** vorausgewählt. Mindestens zwei ausgewählte Tage einschließlich des PDF-Enddatums sind erforderlich. Die Gesamtsummen werden zur Kontrolle gegenübergestellt.
- **Ticketnummer nur nach Bestätigung:** Erst wenn „Ausgewählte Tage prüfen und fehlende Ticketnummern übernehmen“ ausdrücklich gewählt und der Import abschließend gespeichert wird, ergänzt die App fehlende Tickets ausschließlich an den ausgewählten Tagen. Bestehende Tickets, Tageskilometer, Zeiten und Pausen bleiben unverändert. PDF-Prüfnachweise werden für die ausgewählten Tage gespeichert.
- **Keine Datenbankmigration:** Die bisherige `wochenberichte.db` bleibt verwendbar; Service-Worker-Version wurde auf V2.24.2 angehoben. Vor dem Update Datenbank sichern.

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

Den **gesamten Inhalt des ZIP** im Root von `Oxijan86/Wochenbericht-Erstellung-` hochladen. Mindestens `index.html` und `sw.js` gemeinsam ersetzen; zusätzliche Dokumentations- und Testdateien können ebenfalls überschrieben werden. `.nojekyll` unverändert belassen. Auf Android bzw. am PC nach dem Deployment neu laden (bei installiertem Offline-App-Icon ggf. App schließen und erneut öffnen). Die neue App zeigt **Version 2.24.2** an.

**Niemals** Browser-Sitedaten bzw. IndexedDB löschen, um einen veralteten Offline-Cache zu bereinigen. Vorher separate `wochenberichte.db`-Datei sichern. Bestehende Datenbankstruktur wird durch dieses Update nicht migriert.

## Testgrenzen

Automatisierte Chromium-Tests mit PC- und mobilem Viewport sind keine Prüfung auf einem realen Android-Gerät. Produktive OneDrive-Synchronisation, echte RONDO-PDFs und die produktive Datenbank wurden aus Datenschutz- und Zugriffsgründen nicht getestet. Details und Reproduktionsmöglichkeiten in `TESTPROTOKOLL.md`.

### V2.24.4
RONDO-PDF: Korrekte Kunden-/Technikerzuordnung und Mehrtagesabgleich auch bei Straßenangabe im Einsatzort.
