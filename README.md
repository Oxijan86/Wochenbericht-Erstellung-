# Wochenbericht Lovrencic – Version 2.11.0

Standalone-HTML-Anwendung für Servicetechniker mit IndexedDB, SQLite-Datei `wochenberichte.db`, Import von M365-Ergebnissen und historischen Excel-Wochenberichten sowie Excel-Export in der ursprünglichen Wochenberichtvorlage.

## Neu in 2.11.0

- **Automatischer Importabgleich:** Bei mehreren alten Excel-Wochenberichten bzw. M365-Zeilen werden bereits identische Einsätze ohne weitere Abfrage übersprungen. Neue Einträge werden gesammelt vorgemerkt. Nur bei echten Abweichungen oder unsicheren Kundenzuordnungen wird nachgefragt.
- **Sammelauswahl:** Eindeutige Abweichungen gesammelt zur Aktualisierung auswählen; offene Prüffälle gesammelt überspringen oder zurücksetzen. Unklare Filialen werden nicht automatisch zugeordnet.
- **Korrekte Vergleichsdaten:** „Bisher gespeichert“ bezeichnet stets den konkret gewählten Datensatz aus der lokalen Arbeitsdatenbank des aktuellen Technikers. Der Cloud-Dateistand wird dadurch nicht unmittelbar abgefragt; dafür zuvor synchronisieren bzw. den aktuellen Ordnerstand laden.
- **Altdaten bleiben:** Unverändertes `wochenberichte.db`-Datenbankformat und identischer Excel-Export; vorhandene Daten werden nicht neu erstellt oder überschrieben.

## Funktionen aus Version 2.10.0

- **Excel-Archivimport**: Im Reiter **M365 & Datenimport** lassen sich mehrere fertig ausgefüllte Wochenberichte `.xlsx` und `.xlsm` gemeinsam auswählen und auslesen – unabhängig von Kalenderwoche und Jahr. Unterstützt ist die Originalspaltenfolge Datum/Ticket/Kunde–Ort/km/Reisezeit/Beginn/Ende/Arbeitszeit. Ältere `.xls`-Dateien vorher als `.xlsx` speichern.
- **Vergleich vor Speicherung**: Der Excel-Import verwendet denselben bestätigungspflichtigen Dublettenabgleich wie M365. Bestehende manuelle Uhrzeiten werden nicht ungefragt ersetzt, können in der Vorschau aber korrigiert werden. Zusammenfassungs- und Tagessummenzeilen werden nicht als Einsätze übernommen.
- **Kundenstamm**: Aus den Berichtszellen auslesbare Kunden, Einsatzorte, Kilometer und Reisezeiten werden nach bestätigter Speicherung in den Kundenstamm übernommen. Nicht im Excel-Bericht vorhandene Anschriften oder Kundennummern werden nicht erfunden.
- **Kompaktere Erfassungsoberfläche**: Weniger Beschreibungstexte direkt unter Eingabefeldern. Die Hinweise stehen im Hilfe-Reiter.
- **Cloud-Ordnerdiagnose**: Beim Start wird der gespeicherte Dateihandle ohne Berechtigungsdialog geprüft. Ist er noch vorhanden, aber der Zugriff verweigert, wird „Ordnerzugriff erneut freigeben“ angeboten. Ist die Verknüpfung verloren, den **gleichen** Ordner neu auswählen. Revisions- und Datenbank-ID-Abgleich verhindert ein stilles Überschreiben bei abweichenden Datenständen.

## Einrichtung und Veröffentlichung

Die Anwendung kann als `index.html` und `sw.js` auf GitHub Pages veröffentlicht werden. `index.html` ist eine vollständige Anwendung und braucht keine CDN-Abhängigkeiten. Die Datei `.nojekyll` aktiviert die direkte Bereitstellung ohne Jekyll.

Für GitHub-Updates `index.html`, `sw.js`, `README.md` und `.nojekyll` im Stammverzeichnis des Repositories aktualisieren und Pages unter **Settings → Pages → Deploy from a branch → main / root** aktiv lassen.

Die lokale Datenbank wird unter derselben Browser-Origin in IndexedDB gespeichert. Bitte vor dem Update die `wochenberichte.db` herunterladen. Die `wochenberichte.db` wird **nicht** mit dem öffentlichen GitHub-Repository hochgeladen.

## Cloud-Ordner: wichtig

Browser-Ordnerberechtigungen können nach dem Neustart erneut erforderlich sein. Ein synchronisierter OneDrive-/Google-Drive-Ordner ist nicht dasselbe wie der Zugriff über die Cloud-App: Der Browser muss diesen Ordner tatsächlich öffnen dürfen. Gerade auf Android ist eine dauerhafte Ordneranbindung häufig nicht unterstützt. Verwende dann Download und Import der `.db` zwischen Geräten.

Browser-Speicher ist ursprungsabhängig: Die HTML-Datei als `file://`, `github.io`, private Tabs und andere Domains teilen ihre IndexedDB-Daten und Ordnerverknüpfungen nicht. Website-Daten löschen kann lokale Daten und gespeicherte Ordnerhandles entfernen. Für automatische Cloud-Ordnersynchronisation zuerst auf dem einen Gerät synchronisieren und dann auf dem anderen den aktuellen Dateistand laden. Es gibt keine serverseitige Gleichzeitigkeitssperre.

## Sicherheit und Grenzen

Die Excel-Dateien werden lokal eingelesen und nicht verändert. Makros aus `.xlsm` werden nicht ausgeführt. Unbekannte Tabellenformate und beschädigte Dateien werden abgewiesen; die Anwendung prüft vor dem Import alle Dateien und erzeugt erst nach ausdrücklicher Bestätigung neue Einsätze.

Die Original-Excel-Ausgabe bildet weiterhin Montag bis Freitag und maximal sechs Tageszeilen ab. Zusätzliche Wochenend- oder Überlaufeinsätze erscheinen in der ergänzenden Datenübersicht. Diese Begrenzung gilt nicht für die Datenbank.

## Tests

Siehe `TESTPROTOKOLL.md`. Ein echter Android-, OneDrive- oder Google-Drive-Mehrgeräte-Funktionstest wurde hier nicht durchgeführt.
