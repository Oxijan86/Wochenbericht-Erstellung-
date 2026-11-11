Wochenbericht Lovrencic – Version 2.25.15
Datum: 11.11.2026

NEU
1. PDF-Vergleich der Arbeitszeit, Reisezeit und Kilometer für einzelne oder mehrere zugeordnete Einsatztage. Die Gegenüberstellung zeigt PDF-Gesamtwert, manuell erfasste Summe und Differenz (manuell minus PDF). Keine Kilometerangabe in der PDF wird als "Nicht angegeben" dargestellt, nicht als 0 km. Fehlende Tagesangaben werden nicht fälschlich als 0 km gewertet.
2. Auf Mobilgeräten sind die einzelnen PDF-Leistungspositionen immer sichtbar und auswählbar – auch bei eindeutig zugeordnetem Techniker. Positionsart, Hauptticket/Unterticket, Beschreibung und Wert werden in Karten dargestellt; Markierungen aktualisieren die Summen sofort.
3. Nach einer bestätigten und erfolgreich synchronisierten Ordnerdatei blendet die App die Speicher-/Sync-Abfrage automatisch aus. Bei weiteren lokalen Änderungen wird die Abfrage wieder eingeblendet; bei Problemen oder Konflikten bleibt sie sichtbar.
4. Bei bereits PDF-geprüften mehrtägigen Einsätzen enthält die aufklappbare Wochenansicht zusätzlich die Gegenüberstellung aller drei Werte mit Kilometerabweichung.

INSTALLATION IN GITHUB
- Vorher bestehende wochenberichte.db speichern/synchronisieren und zusätzlich ein Backup anlegen.
- ZIP auf deinem Gerät ENTpacken.
- Nur diese fünf Dateien in das Stammverzeichnis des GitHub-Pages-Repositories hochladen und vorhandene Versionen ersetzen:
  index.html, sw.js, manifest.webmanifest, icon-192.png, icon-512.png.
- Auf dem Branch main "Commit changes" bestätigen.
- Unter Actions prüfen, dass "pages build and deployment" erfolgreich ist.
- Die veröffentlichte PWA neu öffnen und prüfen, ob Version 2.25.15 angezeigt wird.
- Falls weiterhin die alte Version angezeigt wird: PWA schließen und erneut öffnen, ggf. im Browser die Seite mit aktualisiertem Seiteninhalt laden. Keine Website-/Browser-Daten löschen.

DATENSCHUTZ / DATENBANK
- Keine Datenbankdatei im ZIP. Keine Änderung der Datenbankstruktur.
- Es werden keine gespeicherten Uhrzeiten, Reisezeiten oder Kilometer automatisch mit PDF-Gesamtwerten überschrieben.
- Cloud-Ordnerberechtigungen und Konfliktfreigaben bleiben von den Sicherheitsregeln des Browsers abhängig.

GRENZEN DER TESTS
- Browser-JavaScript wurde in Chromium (Desktop und Smartphone-Breite) geprüft, außerdem das Auslesen von drei RONDO-Test-PDFs.
- Die echte Edge-PWA auf deinem Smartphone und dein produktiver Cloud-Ordner wurden nicht direkt getestet. Das erstmalige Testen einer echten Cloud-Synchronisierung und Wiederherstellung muss vor der produktiven Nutzung kontrolliert werden.

ZUSÄTZLICH: VERSTÄNDLICHE CLOUD-KONFLIKTLÖSUNG
5. Unter „Speicherung & Sync“ → „Dateistände vergleichen“ erscheinen jetzt Unterschiede zwischen lokalem und Cloud-Stand nach Einsatz und Feld, ergänzt um abweichende Wochenwerte, Kunden und Profile.
6. Zu einem Unterschied kann jeweils die lokale Variante, die Cloud-Variante oder bei einfachen Feldern ein selbst korrigierter Wert ausgewählt werden. Ein nur auf einer Seite vorhandener Einsatz bleibt zunächst erhalten. Entscheidungen sind explizit; keine automatische Übernahme nur nach Zeitstempel.
7. Bei möglicher doppelter Erfassung desselben Einsatzes (gleicher Tag/Ticket oder Kunde, gleiche Uhrzeiten, aber verschiedene Kennungen) erscheint eine zusätzliche Warnung und eine separate Bestätigung. Zum Entfernen einer doppelten Buchung den Haken „Eintrag behalten“ am betreffenden Eintrag entfernen.
8. Vor einer Zusammenführung werden der lokale und der Cloud-Originalstand unabhängig als .db in den Gerätesicherungen abgelegt. Die Zusammenführung wird ZUERST nur lokal gespeichert. Die Cloud wird erst durch die separate Schaltfläche „Prüfen und ausdrücklich veröffentlichen“ ersetzt und der ersetzte Stand in den Backup-Ordner kopiert.
9. Vor der Veröffentlichung wird die Cloud-Revision erneut kontrolliert. Ist zwischen Vergleich und Veröffentlichung eine andere Änderung erfolgt, wird die Veröffentlichung verweigert. Offene, ungespeicherte Formulare und PDF-Importe blockieren die Zusammenführung.
10. Bei nachweisbar nur lokal geändertem Stand erhältst du eine entsprechende Empfehlung. Haben beide Geräte unabhängig gespeichert, entscheidet nicht das Änderungsdatum, sondern du prüfst die Unterschiede. Eine ausstehende Cloud-Synchronisierung wird nicht als abgeschlossen angezeigt.

WICHTIG BEIM GERÄTEWECHSEL
- Smartphone: Einsatz speichern und die Cloud-Bestätigung wirklich abschließen.
- PC: Vor der ersten Bearbeitung den Cloud-Stand prüfen und synchronisieren.
- Bei Konflikt: „Dateistände vergleichen“ wählen, nicht „Lokalen Stand ausdrücklich übernehmen“, bevor du die Unterschiede kontrolliert hast.
- Die echten Geräteordner und OneDrive-/Edge-Berechtigungen lassen sich im Testsystem nicht ersetzen. Nach dem Update einmal mit einem Datensatz und gesicherten Originaldateien testen.
