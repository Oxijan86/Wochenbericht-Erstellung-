# Wochenbericht Lovrencic – Version 2.8.0

GitHub-Pages-fähige, offline nutzbare Wochenbericht-Anwendung für Service-Techniker. SQLite-Datei `wochenberichte.db` / IndexedDB, Excel-Export im Originalformat, Kundenhistorie, Backup, Datensynchronisation und M365-Vorschau.

## Neu: Serviceberichte aus beliebigen Kalenderwochen gemeinsam importieren

**Die aktuell im oberen Bereich ausgewählte Kalenderwoche schränkt den Import nicht mehr ein.**

1. In M365 mehrere Serviceberichte gleichzeitig auswerten lassen und das gemeinsame Ergebnis als TAB-getrennte Zeilen mit neun Spalten kopieren.
2. Unter **M365 & Datenimport** alle Zeilen zusammen in das Textfeld einfügen und **Daten prüfen** wählen. Auch Berichte aus anderen Kalenderwochen oder Jahren werden erkannt.
3. Jede Importzeile wird anhand ihres Datums der **richtigen ISO-Kalenderwoche** des aktuell gewählten Technikers zugeordnet. Die Vorschau zeigt die Ziel-KW an.
4. Findet die Anwendung am gleichen Datum einen bestehenden Einsatz (gegebenenfalls mit ähnlich geschriebenem Kundennamen), vor dem Speichern zwischen **Aktualisieren**, **Neu anlegen** und **Überspringen** entscheiden.
5. Vor dem Aktualisieren können Kilometer, Reisezeit, Ticket, Bemerkungen **sowie Beginn und Ende** in der Vorschau bearbeitet werden. Vorhandene manuelle Uhrzeiten werden vorausgefüllt; Datum und Datensatzkennung bleiben beim Aktualisieren erhalten.
6. Erst **Auswahl bestätigen und speichern** übernimmt alle akzeptierten Zeilen in einem gemeinsamen lokalen Speichervorgang über die betroffenen Wochen. Bei einer ungültigen Zeile wird **nichts aus dem aktuellen Stapel übernommen**. Die aktuell angezeigte KW bleibt unverändert.
7. Danach sind die Einträge in **Einsatzdaten (alle Monate)** bzw. durch Wechsel in die betreffende Kalenderwoche sichtbar.

### Hinweis zum Original-Excel-Bericht

Die bestehende Originalvorlage besitzt pro Montag–Freitag je sechs Einsatzzeilen. Die Anwendung speichert auch Samstag- und Sonntagseinsätze in der jeweiligen ISO-Woche und zeigt sie in der Historie; diese lassen sich **nicht** in der unveränderten Excel-Vorlage abbilden. Damit nichts stillschweigend fehlt, wird der Excel-Export einer solchen Woche mit einem verständlichen Hinweis abgebrochen. Sie müssen die Wochenendstunden für einen gesonderten Bericht behandeln.

### Update aus V2.7

- Das Datenbankschema wurde **nicht** geändert, vorhandene Profile, Einsätze, Kundenstamm, Entwürfe, Sync-Verknüpfungen und Backups bleiben kompatibel.
- Vor dem Update eine Sicherung von `wochenberichte.db` erstellen.
- In deinem GitHub-Repository die Dateien aus dem Schnellupload-Paket **entpackt** ersetzen: `index.html`, `sw.js`, `README.md`, `.nojekyll`. GitHub Pages bleibt auf `main` / `/ (root)`.
- Der Service-Worker-Cache heißt `wochenberichte-static-v2.8.0`. Nach dem Update im Kopf **Version 2.8.0** kontrollieren.
- Keine persönlichen Datenbanken oder vollständigen Kundenlisten auf GitHub veröffentlichen. Die Projektdateien sind anonymisiert.

## Grenzen

Die Tests erfolgten in einem isolierten Chromium-Browser bei 390 px Breite mit simulierter Speicherschnittstelle für den UI-Import. Es wurde kein echtes Android-Smartphone, keine reale Cloud-Synchronisation und kein echtes RONDO-PDF getestet. Die Speicherdatei wurde separat durch SQLite-Encode/Decode geprüft.
