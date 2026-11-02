Wochenbericht Lovrencic – PWA Version 2.25.11 (02.11.2026)
==============================================================

GITHUB-PAGES-UPDATE
1. Vor dem Update wochenberichte.db sichern und Synchronisation kontrollieren.
2. Diese fünf Dateien in das Stammverzeichnis von „Wochenbericht-Erstellung“ hochladen bzw. ersetzen:
   index.html
   sw.js
   manifest.webmanifest
   icon-192.png
   icon-512.png
3. „Commit changes“ bestätigen, GitHub Pages aktualisieren lassen.
4. App neu laden und oben Version 2.25.11 kontrollieren.
5. Bestehende Datenbank weiterverwenden, NICHT neu anlegen.

NEU
- Eigenständiger Versand-Excelbericht für Samstag und Sonntag (.xlsx).
  Menü „Wochenbericht / Export“ → KW wählen → „Wochenendbericht (.xlsx)“.
  Gibt es mehrere Wochenend-Einträge in derselben KW, enthält die Datei alle.
- Samstag-/Sonntageinsätze bleiben in Wochenansicht/Historie sichtbar,
  fließen aber nicht in den regulären Wochenstunden-/FZA-Saldo ein.
  Dies gilt auch bei der Übernahme des Startsaldo-Werts der Vorwoche.
- Wochenend-Excel-Bemerkung nur:
  „Samstagseinsatz am ... – gesonderte Vergütung/Abrechnung für Wochenendeinsätze.“
  (sonntags entsprechend Sonntagseinsatz.)
  Kein PDF-Buchungsdatum oder interne Stundensaldo-Hinweise in der Bemerkung.
- RONDO-PDF-Hauptticket plus Unterticket: Arbeitszeitpositionen nur einmal
  zählen und gemeinsam anzeigen, jedoch bei Untertickets den Techniker
  ausdrücklich kontrollieren.
  Musswessels Ticket 28553: Hauptticket 5:00, Unterticket 28552: 3:00,
  bei Zugehörigkeit zum selben Techniker Gesamt 8:00 Arbeitszeit.
- Bisherige Mehrtageseinsätze, manuelle Datumswahl, 28-Tage-Aufhebung
  und PDF-Personentrennung bleiben erhalten.

WICHTIGER HINWEIS ZUR VERGÜTUNG
Die Trennung entspricht den Vorgaben des Nutzers. Die tatsächliche Abrechnung
richtet sich nach den geltenden betrieblichen Vereinbarungen. Der Export
verändert keine Lohnabrechnungsdaten außerhalb dieser App.

ZUSATZDATEI
„Beispiel_Samstagseinsatz_Stinges_17-10-2026.xlsx“ dient als sofort
versendbare separate Excel-Datei und muss NICHT auf GitHub hochgeladen werden.
