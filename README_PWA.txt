Wochenbericht Lovrencic – PWA Version 2.25.9 (02.11.2026)

Installation/Update auf GitHub Pages:
1. Vorher wochenberichte.db sichern und mit deinem Ordner synchronisieren.
2. Die fünf Dateien index.html, sw.js, manifest.webmanifest, icon-192.png und icon-512.png im Stammordner deines GitHub-Pages-Projekts hochladen. Vorhandene Dateien mit denselben Namen ersetzen.
3. Änderungen per Commit bestätigen. Falls in der PWA noch 2.25.8 steht, Seite neu starten und die aktualisierte PWA-Version prüfen.
4. Ein PDF auswählen: Der Status nennt jetzt sofort die Anzahl der PDFs. Auf „PDF-Dateien auslesen und abgleichen“ klicken; danach die Vorschau prüfen und mit „Berichtsauswahl prüfen und Einsätze vergleichen“ fortfahren.
5. Das eigentliche Speichern erfolgt weiterhin erst über die bestätigte Import-Übernahme. PDF-Gesamtstunden werden niemals automatisch auf einzelne Tage verteilt.

Version 2.25.9 behebt das versehentliche Entfernen zweier PDF-Klickhandler in Version 2.25.8. Eine neue Dateiauswahl leert alte, ungespeicherte PDF-Vorschauen (nicht die Datenbank). Einzelne ungültige PDF-Dateien werden für den Benutzer separat angezeigt.

Hinweis: Die PWA-Installation und Cloud-Ordnerrechte sind vom jeweiligen Browser abhängig. Die Tests erfolgten in Chromium mit simuliertem Datenbestand; ein produktiver Edge-Cloud-Test ist nicht möglich.

Version 2.25.10: PDF-Dateien ohne Positionsdatum werden gelesen; Einsatzdatum ist vor Vergleich manuell einzugeben. 28-Tage-Grenze für Vorschläge entfernt.
