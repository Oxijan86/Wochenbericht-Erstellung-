Wochenbericht Lovrencic – PWA 2.25.13 (Hotfix)
================================================

FEHLERBEHEBUNG
- Der Startfehler "y is not defined" beim Wiederöffnen einer bestehenden Datenbank
  wird durch die korrigierte Exportprüfung verhindert.
- Die reguläre Excel-Summenberechnung berücksichtigt nur reguläre Einsätze;
  Werktags-Sondereinsätze und Wochenendeinsätze werden nicht mehr in den
  Excel-Gesamtsummen mitgezählt.
- Startfehlermeldung nennt nicht länger pauschal Browserberechtigungen als Ursache.

Vorhandene SQLite-Datenbanken und Exportvorlagen werden nicht verändert.

GITHUB PAGES
Genau diese fünf Dateien im bestehenden Repository ersetzen:
index.html, sw.js, manifest.webmanifest, icon-192.png, icon-512.png.
Danach im Browser kontrollieren, ob oben Version 2.25.13 angezeigt wird.
Möglicherweise sind PWA-Dateien noch zwischengespeichert: dann App vollständig
schließen und neu laden. Vor dem Upload möglichst bestehende wochenberichte.db sichern.

WICHTIG: Bei der Fehlermeldung "y is not defined" keine neue Datenbank anlegen
und keine Browserdaten löschen. Die Daten sind nicht ursächlich für den Fehler.
