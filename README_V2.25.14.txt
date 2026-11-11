WOCHENBERICHT LOVRENCIC – PWA VERSION 2.25.14
Stand: 11.11.2026

INSTALLATION AUF GITHUB PAGES
1. Vorher in der bisherigen App den Datenbankstand sichern: wochenberichte.db herunterladen und möglichst ordnungsgemäß synchronisieren.
2. ZIP entpacken. Die fünf PWA-Dateien index.html, sw.js, manifest.webmanifest, icon-192.png und icon-512.png im Wurzelordner deines bestehenden GitHub-Pages-Repositories ersetzen; keine neue Datenbank hochladen.
3. Commit changes bestätigen, anschließend Anwendung neu öffnen und Versionsanzeige 2.25.14 kontrollieren.
4. Bei einer installierten PWA kann der Service-Worker-Cache eine ältere Version zeigen. Bei Bedarf die Live-Seite öffnen und die PWA erneut starten. KEINE Browserdaten löschen und KEINE neue Datenbank erstellen.

NEU IN VERSION 2.25.14
- Direkt nach explizitem Speichern erscheint eine nicht blockierende Synchronisierungsleiste mit „Jetzt synchronisieren“, „Später“ und – nur bei bestätigtem Konflikt – „Lokalen Stand nach Sicherung übernehmen“.
- Ordnerberechtigung kann über diese Leiste neu angefordert werden. Die Web-App kann die Android-/Edge-Berechtigungsabfrage nicht unterdrücken.
- Vor einem bewussten Überschreiben wird die bisherige Ordnerdatei im Backup-Verzeichnis sowie lokal gesichert. Unterschiedliche Datenbankidentitäten werden weiterhin blockiert.
- Die PDF-Abgleichssuche bietet alle vorhandenen Einsätze am manuell gewählten tatsächlichen Leistungsdatum an: auch mit falschem, abweichendem oder fehlendem Kundenname und Ticket. Keine automatische Zuordnung allein anhand des Datums.
- Beim mehrtägigen Abgleich zeigt die Auswahl alle gespeicherten Einsätze an den eingegebenen tatsächlichen Einsatzdaten. Alle Kontrollkästchen sind zunächst leer.
- Für jeden ausgewählten Einsatztag kann gesondert „Kunde, Ticket und Ort aus PDF übernehmen“ bestätigt werden. Uhrzeiten, Pausen, Reisezeiten und Kilometer bleiben unverändert.
- Beim eintägigen PDF-Abgleich gibt es einen Button zum Übernehmen von Kunde, Ticket und Ort; dokumentierte Kilometer und Reisezeiten werden standardmäßig beibehalten.
- Beim manuellen Ändern eines gespeicherten Kundennamens bleibt die bestehende Ticketnummer erhalten, wenn sie im Formular leer geworden ist; unveränderte Kilometer werden über eine ausdrückliche Rückfrage beibehalten oder zurückgesetzt.
- Bereits vorhandene freie Datumsauswahl und Mehrtages-Eingabe, 28-Tage-Grenze entfernt, Sonder- und Feiertags-Excel sowie Haupt-/Unterticketzeiten bleiben bestehen.

WICHTIG
„Cloud“ meint in dieser Anwendung eine vom Browser freigegebene Datei im synchronisierten Backup-Ordner. Der Abgleich mit OneDrive oder einem anderen Cloud-Anbieter erfolgt danach über die Synchronisierungssoftware des Geräts. Der Status „Ordnerdatei bestätigt“ ist keine Zusicherung, dass der externe Cloud-Dienst die Datei bereits hochgeladen hat.
Sicherheitsprüfung: Ein ungleicher Cloud-Stand wird NICHT automatisch überschrieben. Nur ausdrücklich bestätigte Konfliktübernahme; der alte Ordnerstand wird vorher gesichert.
