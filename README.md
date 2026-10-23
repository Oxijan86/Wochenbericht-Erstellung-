# Wochenbericht Lovrencic – V2.23.0 (23.10.2026)

Die Anwendung funktioniert im Browser auf PC und Smartphone. Einsatzdaten bleiben in der bestehenden lokalen Datenbank (IndexedDB), mit optionaler Ordnersynchronisation unter „Speicherung & Sync“. **Vor der Aktualisierung bitte eine separate Datenbanksicherung erstellen.**

## Neu in V2.23

- **PDF-Import pro Datei steuern:** Jede erfolgreich ausgelesene PDF erhält die beiden Möglichkeiten „Positionen übernehmen und abgleichen“ und „Diesen Bericht vollständig überspringen“ – auch bei eindeutig erkannten Technikern.
- **Kein zusätzlicher Techniker-Bestätigungshaken:** Bei gemischten Serviceberichten die eigenen Arbeits-, Reisezeit- und Kilometerpositionen auswählen. Der Klick auf „Berichtsauswahl prüfen und Einsätze vergleichen“ bestätigt die jeweilige Auswahl für die Vorschau. Die Daten werden erst beim abschließenden „Auswahl bestätigen und speichern“ dauerhaft übernommen.
- **Überspringen ohne erneute Dateiauswahl:** Die übrigen PDFs bleiben im Stapel. Wenn alle PDFs übersprungen werden, kehrt die Anwendung ohne Datenänderung zur PDF-Auswahl zurück.
- **Sicherheitsprüfung bleibt erhalten:** Ohne markierte Positionen kann ein Bericht nur übersprungen, nicht als leerer Einsatz übernommen werden. Kaputte PDFs müssen weiterhin ausdrücklich ausgeschlossen werden.

## Aus V2.22

- Kalenderwoche und Stundenübersicht nur in „Einsätze erfassen“ und „Wochenbericht / Export“.
- Nach Eingabe des Arbeitsbeginns erscheint ein automatisch berechneter Vorschlag zum Arbeitsende anhand der PDF-Dauer und einer möglichen Pause; manuelle Endzeiten werden nicht überschrieben.

## Aus V2.21

- **PDF-Arbeitsdauerabweichungen sind nur noch Kontrollhinweise.** 15–29 Minuten werden als Hinweis angezeigt; ab 30 Minuten erscheint ein deutlicher Warnhinweis mit den beiden Dauern und der Differenz. Der Excel-Export ist deswegen **nicht** gesperrt und es ist keine Ausnahmebegründung erforderlich.
- **Fehlende tatsächliche Beginn-/Enduhrzeiten** sind weiterhin eine eigene Vollständigkeitsprüfung: Zunächst den Einsatz nachtragen oder eine begründete Ausnahme bestätigen. Ungültige Pausen können weiterhin blockieren.
- **Frühere Serviceberichte regulär importieren:** Der zusätzliche Modus „Nur Kundenstamm ergänzen“ entfällt. Alte PDFs werden nach Datum in der Einsatzhistorie gespeichert oder mit bestehenden Einsätzen abgeglichen. Es bleiben manuelle Prüfungen bei unklarer Zuordnung und eine Dublettenprüfung; fehlende Kundenadressen werden ergänzt.
- Vorhandene manuelle Uhrzeiten, PDF-Prüfnachweise, Rücksprung nach Zeitkorrektur und Synchronisations-Konfliktschutz bleiben erhalten.

## Benutzung

1. Servicebericht-Import öffnen und mehrere aktuelle oder ältere PDFs einlesen. Pro PDF entweder die passenden Technikerpositionen kontrollieren oder „Diesen Bericht vollständig überspringen“ wählen. Danach „Berichtsauswahl prüfen und Einsätze vergleichen“ und abschließend „Auswahl bestätigen und speichern“ betätigen.
2. Unter „Wochenbericht / Export“ die Exportprüfung lesen. Bei PDF-Stundenabweichungen wird die Differenz gezeigt und der Einsatz kann direkt kontrolliert werden, der Export bleibt möglich.
3. Bei fehlenden Uhrzeiten über „Einsatz korrigieren“ nachtragen oder ausdrücklich eine begründete Ausnahme zulassen.

## Wichtige Grenzen

Die Original-Excel-Vorlage bietet sechs Einsatzzeilen pro Wochentag (Mo–Fr); weitere Einsätze stehen in einer ergänzenden TSV-Übersicht. Serviceberichte enthalten typischerweise **Netto-Arbeitsdauer, nicht Beginn/Ende**. Unterschiede können sachliche Gründe haben. Eine geräteübergreifende OneDrive-Synchronisation wurde nicht end-to-end getestet, und für den PDF-Parser lagen keine neuen originalen RONDO-Berichte vor.

## GitHub Pages

`index.html`, `sw.js`, `README.md` und `.nojekyll` aus dem Schnellupload in das Wurzelverzeichnis der GitHub-Pages-Quelle hochladen. Cache-Kennung `wochenberichte-static-v2.23.0`. Bei alter Darstellung Seite neu laden; Browserdatenbank **nicht** löschen.


## V2.22
- KW-Konfiguration und Stundenübersicht nur bei „Einsätze erfassen“ und „Wochenbericht / Export“.
- PDF-Endzeitvorschlag nach Eingabe Arbeitsbeginn: netto PDF-Arbeitsdauer plus Arbeitspause.
- Vorschlag bleibt bis zum Speichern ausdrücklich gekennzeichnet; bestehende Endzeiten werden nicht überschrieben.
