# Wochenbericht Lovrencic – Version 2.14.0

Offlinefähige HTML-Anwendung für Serviceeinsätze, Fahrt-/Arbeitszeiten, Pausen, den originalen Excel-Wochenbericht und den PDF-, Excel- und M365-Import.

## Neu: Kundenbezogene Startvorschläge

- Im Dashboard „Neuen Einsatz erfassen“ öffnen und im Einsatzassistenten einen **gespeicherten Kundenstandort** wählen. Bereits erfasste Kunden und Standorte bleiben unterscheidbar, auch wenn der Kundenname gleich ist.
- Aus der letzten passenden **vollständig abgeschlossenen Rundfahrt** des ausgewählten Technikers werden die Gesamt-Kilometer und Gesamt-Reisezeit **halbiert** und als editierbarer Hinfahrt-Vorschlag eingetragen. Wenn keine verlässlichen Rundfahrtdaten vorliegen, darf auch ein eindeutig diesem Techniker zuordenbarer Kundenstammwert verwendet werden. Unvollständige Fahrten oder Daten eines anderen Technikers sind keine Grundlage für automatische Vorschläge.
- Bei ungeraden Gesamtminuten wird der Halbwert auf eine ganze Minute gerundet, bei ungeraden Kilometern sind 0,5 km im Assistenten erlaubt. Die tatsächlichen Werte können korrigiert werden.
- **Vorschläge gelten nicht als bestätigte gefahrene Kilometer/Zeit**. Erst nach bestätigter Ankunft werden sie als Hinfahrt gespeichert und in Wochenstatistiken berücksichtigt.
- Der Kunde und der hinterlegte Ort werden in der Eingabemaske übernommen. Bei abweichendem Ort wird vor dem Anlegen eines neuen Kundenstandorts nachgefragt. Ein bestehender Datensatz kann weiterhin unter „Kunden → Bearbeiten“ korrigiert werden. Ein anderer Standort erhält einen getrennten Eintrag und übernimmt **nicht** automatisch die alte Adresse.
- In der Kundenliste startet „Für neuen Einsatz“ einen bereits vorausgefüllten Fahrtenassistenten; wenn derselbe Kunde bereits einen laufenden Einsatz hat, wird dieser geöffnet. Bei „Navigation öffnen“ wird gefragt, ob der passende Einsatz zugleich gestartet oder fortgesetzt werden soll.
- Wie bisher: Nach Arbeitsende werden die Hinfahrtwerte für die Rückfahrt vorgeschlagen und können geändert werden; Pausen und Kundenwechsel bleiben vorhanden.

## Neu: Speicher- und Synchronisierungsstatus

- Der **kompakte, anklickbare Speicherstatus** befindet sich ausschließlich in der **blauen Kopfzeile**. Er unterscheidet lokal gespeichert, lokale Speicherung läuft/fehlerhaft, Synchronisierung läuft/offen, Ordnerzugriff fehlt und ordnerseitig geprüft synchronisiert.
- Detaillierte Ordnerverknüpfung, Berechtigungen, Dateikonflikte und Aktionen befinden sich nur unter „Speicherung & Sync“. Die bisherige obere Cloud-Karte und die redundante Dashboard-Speicherkarte entfallen.
- Nach der **ausdrücklich bestätigten Übernahme** aus RONDO-PDFs wird die gesamte Datenbank zunächst lokal in IndexedDB gespeichert. Unmittelbar anschließend wird eine zusätzliche lokale DB-Sicherung erstellt. Ist ein lokaler/Cloud-Synchronisationsordner verbunden, wird die Datei geschrieben und ihre Revision wieder eingelesen/verifiziert. Die Übernahme zeigt ausdrücklich an, ob dies gelungen ist.
- Bei einem Ordner-/Berechtigungsfehler **wird die lokal gespeicherte Übernahme nicht verworfen**. Die Kopfzeile und die Importmeldung warnen, dass die Ordnersynchronisierung nicht bestätigt wurde. Die fehlgeschlagene Ordnerfreigabe lässt sich unter „Speicherung & Sync“ nachholen.
- **Wichtig:** Eine nachgeprüfte Datei im synchronisierten Ordner bestätigt noch nicht den Upload durch OneDrive/Google Drive ins Internet. Diesen Transfer steuert der Cloud-Anbieter und der Browser kann Ordnerberechtigungen auf Android verlieren.

## Kompatibilität und Import

Das Datenbankformat (SQLite-Datei mit Anwendungsdaten) bleibt kompatibel; zusätzliche optionale Felder im Kundenstamm können bisherige Datenbanken erweitern. Die bisherigen PDF-, M365- und Excel-Einlesewege sowie die Original-Excel-Exportvorlage bleiben erhalten. Unklare PDF-Technikerpositionen erfordern weiterhin eine manuelle Bestätigung. Keine stillschweigende Überschreibung von Cloud-Konflikten.

## GitHub Pages

`index.html`, `sw.js`, `README.md` und `.nojekyll` aus dem Schnellupload-Paket ins Stammverzeichnis des Repositorys hochladen. Cache-Version: `wochenberichte-static-v2.14.0`. Nach dem Update sollte die Kopfzeile „Version 2.14.0“ zeigen. Das GitHub-Repository wird nicht automatisch geändert.

**Vor dem Update bitte `wochenberichte.db` sichern.**

## Tests und Grenzen

- JavaScript-Syntaxprüfung, 31 bestehende Rechen-/Excel-Tests sowie Browserprüfungen (390 px) für Kundenwahl, Standorttrennung, Halbierung und Statusanzeigen durchgeführt.
- Ein vollständiger Import-Speicherpfad wurde mit **simulierten** lokalen/Cloud-Schnittstellen geprüft: erfolgreich bestätigte Synchronisierung und verweigerte Berechtigung; bei Letzterer bleiben lokale Änderungen erhalten.
- Keine echte OneDrive-/Google-Drive-Synchronisation und kein Neustarttest auf einem realen Android-Gerät durchgeführt. Die isolierte Browserumgebung blockierte lokale URL-Aufrufe beim Versuch eines vollständigen IndexedDB-Neustarttests.
