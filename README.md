# Wochenbericht Lovrencic – Version 2.14.0

Offlinefähige HTML-Anwendung für Techniker: laufende Einsätze, Fahrt- und Arbeitszeit, RONDO-PDF-Import, Excel-Altberichtimport, M365, Kundenstammdaten, ursprünglicher Excel-Wochenbericht und optionaler Cloud-Ordner.

## Neu in V2.14

- **Navigation mit Einsatzstart:** Unter **Kunden → Navigation starten** zuerst auswählen, ob **„Einsatz starten & navigieren“** oder **„Nur Navigation öffnen“**. Ein neuer Einsatz speichert den Abfahrtszeitpunkt und den ausgewählten Kunden, ohne Fahrtkilometer/-zeiten zu erfinden. Kilometer, Reisezeit und Uhrzeiten können später ergänzt/korrigiert werden. Auch der anfänglich gespeicherte Abfahrtszeitstempel ist korrigierbar; bei einem Datumswechsel wird der Einsatz zur zutreffenden Kalenderwoche verschoben. Während bereits ein Einsatz läuft, verhindert der Navigationsdialog einen unbemerkten zweiten Einsatz und bietet Fortsetzen oder reine Navigation an. Android erhält einen systemüblichen `geo:`-Link für installierte Karten-Apps; iOS Apple Karten; andere Plattformen OpenStreetMap. Der Zielkunde erhält im Einsatzassistenten zusätzlich einen direkt antippbaren Navigationslink. Ein Webbrowser kann nicht garantieren, dass die bevorzugte App installiert ist oder den Wechsel immer automatisch gestattet.
- **Pausen an jedem Einsatzschritt:** Pause starten und fortsetzen für laufende Reise-/Arbeitszeit. Zusätzlich „Pause nachtragen“ für Arbeits- oder Reisezeit, z. B. `030` = 30 Minuten. Manuelle Pausen werden getrennt gespeichert und nur einmal der gewählten Zeitart abgezogen; auch nach Schließen des Assistenten bleiben bestätigte Pausen erhalten.
- **Fahrtvorlagen ohne ungewolltes Überschreiben:** Kilometer/Reisezeit einer einzelnen Fahrt werden nicht automatisch als Kunden-Standardstrecke gespeichert, besonders nicht bei Fahrten von Kunde A zu Kunde B. Wer möchte, kann die Fahrt als Vorlage für genau diese Strecke ausdrücklich speichern und beim nächsten Mal auswählen.
- **PDF-Serviceberichtstatus:** Einsatzdaten/Historie zeigen an, ob ein Servicebericht vorhanden, tatsächlich gegen einen bestehenden Einsatz abgeglichen oder eine Abweichung zu prüfen ist. Ein nur aus einem PDF angelegter Einsatz gilt nicht automatisch als manuell abgeglichen.
- **PDF-Arbeitsuhrzeiten nachtragen:** Die im PDF angegebene Arbeitsdauer wird in der Importprüfung angezeigt. Beginn/Ende können direkt ergänzt oder später ausgelassen und in der KW nachgetragen werden. Es werden keine Uhrzeiten erfunden.
- **Unvollständige Einsätze:** Fehlende Arbeitszeiten, Kunden-/Ortsangaben, Kilometer oder Reisezeiten werden in „Einsätze erfassen“ rot markiert. Je Wochentag bleibt auch bei vorhandenen Einträgen eine Aktion für weitere Einsätze sichtbar.
- **Weniger wiederholte Kopfdaten:** Techniker/KW/Cloud-Status sind nur dort sichtbar, wo sie benötigt werden.
- **Einstellungen:** M365, PDF-Direktimport und Excel-Altdatenimport können getrennt eingeblendet/ausgeblendet werden. Die gemeinsame Prüf-/Speicheransicht bleibt für eingeschaltete Importe benutzbar.
- **Mobile Importprüfung:** Nach Auswertung automatische Navigation zur ersten notwendigen Prüfung; unsichere PDF-Technikerpositionen besitzen eine große Schnellbestätigung an der jeweiligen Karte. Identische Datensätze werden nicht zur Einzelentscheidung angezeigt.
- **Cloud-Schnellaktionen und Konfliktvergleich:** Im Cloud-Modus stehen oben Ordnerfreigabe, Synchronisieren und Vergleichen. Der Vergleich zeigt abweichende Kalenderwochen, Einsätze und Kunden-/Profildaten. Eine Richtung des Überschreibens muss ausdrücklich bestätigt werden, mit Sicherung des überschriebenen Datenstands. Unterschiedliche Datenbankidentitäten werden geschützt.

## Bedienung

1. Unter **Dashboard → Neuen Einsatz erfassen** Hinfahrt starten, beim Kunden Ankunft bestätigen, Arbeit beginnen/beenden, anschließend Rückfahrt oder Folgefahrt zu anderem Kunden auswählen. Bei Abfahrt zum Kunden kannst du alternativ unter **Kunden** die Navigation mit Einsatzstart verwenden.
2. Die Hin- und Rückfahrt werden separat gespeichert. Bei einer gewöhnlichen Rückfahrt erscheinen die Kilometer und die Reisezeit der Hinfahrt als Vorschlag, den du bestätigen oder ändern kannst.
3. Optional Pausen starten/fortsetzen oder nachträglich über die ausklappbare Pause-Eingabe ergänzen. Zeiten wie `130` werden als `1:30` interpretiert, `030` als `0:30`.
4. Unter **Datenimport** RONDO-PDFs, M365-Daten oder Excel-Altberichte auswählen. Nur neue beziehungsweise bewusst bestätigte abweichende Einsätze speichern. Bei unklarer Technikerzuordnung einzelne PDF-Positionen prüfen.
5. Bei Bedarf fehlende Arbeitsbeginn/-endzeiten direkt in der PDF-Importvorschau ergänzen oder später in der KW nachholen.
6. Unter **Einstellungen** unnötige Importarten ausblenden; unter **Speicherung & Sync** Ordnerkonflikte vor einer ausdrücklichen Überschreibung vergleichen.

## Daten- und Formatkompatibilität

Die Datenbankdatei heißt weiterhin `wochenberichte.db`. Neue Angaben sind optionale Attribute an bestehenden Einträgen und Kunden. Die Original-Excel-Vorlage und ihr Montag-bis-Freitag-Layout bleiben unverändert; zusätzliche Wochenend- und Überlauf-Einsätze erscheinen ergänzend im TSV-Export. Vor einer Aktualisierung **immer eine aktuelle `.db`-Sicherung anlegen**.

Die Browser-Datei-Synchronisierung ersetzt keinen echten transaktionalen Cloudserver. Ordnerberechtigungen und die Übergabe an andere Karten-Apps können vom Betriebssystem/Browser abhängen. Vollständige physische Android-/Mehrgeräte-Cloud-Tests wurden **nicht** durchgeführt. Geprüft wurden JavaScript-Syntax, isolierte Browserinteraktionen, fünf digitale RONDO-PDF-Beispiele und bestehende Excel-Berechnungstests (siehe TESTPROTOKOLL.md).

## GitHub Pages

`index.html`, `sw.js`, `README.md` und `.nojekyll` ins Hauptverzeichnis des bestehenden Repositories hochladen. GitHub Pages: Branch `main`, Verzeichnis `/ (root)`. Version und Cache heißen `2.14.0` / `wochenberichte-static-v2.14.0`.
