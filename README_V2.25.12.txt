Wochenbericht Lovrencic – PWA Version 2.25.12
===========================================

INSTALLATION AUF GITHUB PAGES
Nur diese fünf Dateien in den bestehenden GitHub-Pages-Ordner hochladen / ersetzen:
  index.html
  sw.js
  manifest.webmanifest
  icon-192.png
  icon-512.png
Die anderen Dateien sind Dokumentation, Beispiele und NICHT zum Hochladen nötig.

Vor dem Update: wochenberichte.db sichern und bei Cloud-Nutzung synchronisieren.
Nach dem Upload die App neu öffnen und die Anzeige „Version 2.25.12“ kontrollieren.

NEU: Gesonderte Abrechnung an jedem Wochentag
- Unter "Einsätze erfassen" ist das neue Feld "Gesonderte Abrechnung".
- Normaler Einsatz: "Regulärer Einsatz".
- Feiertagseinsatz: "Feiertagseinsatz – separat abrechnen".
- Sonderfahrt / anderer Sondereinsatz: "Sondereinsatz – separat abrechnen".
- Samstag- und Sonntag-Kundeneinsätze werden automatisch separat abgerechnet.
- Ein Feiertagseinsatz wird als Tätigkeit "Kundeneinsatz" erfasst, NICHT als
  Tätigkeit "Feiertag" (das ist ein arbeitsfreier Tag).

Die Einträge bleiben in der Historie und in der Wochenansicht sichtbar.
Bei Sonderabrechnung fließen Arbeits- und Reisezeiten NICHT in die reguläre
Wochenstunden-/Freizeitausgleichsberechnung ein; kein Doppel-Export.

SEPARATER EXCEL-BERICHT
Unter "Wochenbericht / Export" den Button
"Sondereinsätze / Wochenende / Feiertage (.xlsx)" verwenden.
Er enthält die separat abzurechnenden Einsätze der ausgewählten KW.
Bemerkungen: kurzer Hinweis (z.B. "Feiertagseinsatz am 14.10.2026 –
gesonderte Vergütung/Abrechnung.").
Das korrigierte Excel zeigt Beginn und Ende als HH:MM (statt 0,40625 etc.)
sowie Reise-/Arbeits-/Gesamtzeiten als [h]:mm. Die Formel für Gesamtzeit
bleibt erhalten, der Ergebniswert wird vorsorglich auch als Cache geschrieben.

Bestehende SQLite-Datenbankstruktur bleibt unverändert. Die neue Kennzeichnung
wird als optionales Attribut eines Einsatzes im JSON-Nutzdatenbereich abgelegt.

Hinweis: Feiertage werden NICHT ohne ausdrückliche Kennzeichnung automatisch
erkannt, da regionale Feiertagsregelungen und individuelle Abrechnung variieren.
