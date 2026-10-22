# Wochenbericht Lovrencic – Version 2.19.0

Offlinefähige HTML-Anwendung für Servicetechniker, basierend auf Version 2.15. Datenbank, Kundenstamm, RONDO-PDF-Import, optionale Sonderfunktionen, Backups, Synchronisation und originalgetreuer Excel-Export bleiben erhalten.

## Änderungen in V2.19

- **Zeitstempel:** Im Einsatzassistenten sind Beginn und Ende der Hinfahrt, Arbeitszeit und Rückfahrt einsehbar und korrigierbar. Der Assistent speichert die tatsächlichen Zeitstempel. Für den Excel-Wochenbericht werden die Arbeitszeiten weiterhin wie bisher auf Viertelstunden aufgerundet.
- **Hinfahrt:** Reisezeit aus Start-/Ankunftszeit automatisch berechnen, bereits erfasste Fahrpausen abziehen. Optional Reisezeit manuell eintragen oder (bei bekannten Kunden) den früheren Wert als Vorschlag auswählen.
- **Fahrtpausen:** Hinfahrt und Rückfahrt können pausiert und fortgesetzt werden, ebenso die Arbeitszeit. Die Pausen werden dem jeweiligen Zeitkonto zugeordnet.
- **Rückfahrt:** Wahl zwischen automatischer Messung aus den Zeitstempeln, Übernahme der Hinreisezeit und manueller Eingabe. Kilometer sind separat korrigierbar.
- **Kundenwechsel:** Die bestätigte Fahrstrecke und Reisezeit von A nach B werden weiterhin hälftig auf beide Kundeneinsätze verteilt. Die gemessene Dauer berücksichtigt Fahrpausen.
- **Abbrechen:** Laufende Assistenten-Einsätze lassen sich nach Rückfrage endgültig abbrechen. Der begonnene Einsatz wird aus Wochenansicht, Historie und Dashboard entfernt; bei begonnener Weiterfahrt zum nächsten Kunden wird der Vorgängereinsatz wieder in den Zustand „Arbeit beendet“ versetzt.
- **PDF-Abgleich:** Geprüfte Serviceberichte sind mit grünem Haken in der Wochenansicht und Historie gekennzeichnet. Manuelle Nachbearbeitungen widerrufen den bereits erfolgten PDF-Abgleich nicht und lösen keine automatische neue Prüfpflicht aus. Ohne Servicebericht bleibt der Abgleich freiwillig.

## Nutzung

1. Auf PC/Android wie bisher die Anwendung starten. Im Dashboard „Neuen Einsatz erfassen“ klicken – Hinfahrt und Startuhrzeit werden gespeichert.
2. Bei Bedarf „Fahrpause starten“ und anschließend „Fahrt fortsetzen“. Nach Ankunft die Reisezeitmethode wählen; mit „Beim Kunden angekommen“ bestätigen.
3. Arbeitszeit starten, bei Bedarf pausieren, Arbeitsende bestätigen. Die Zeiten stehen im Assistenten zur Korrektur bereit.
4. Rückfahrt starten, bei Bedarf pausieren, bei Ankunft zwischen Zeitstempel-Berechnung, Hinreisevorschlag und manueller Reisezeit wählen und abschließen.
5. Uhrzeiten können auch nach Abschluss im Assistenten berichtigt werden. Ein bereits geprüfter PDF-Beleg bleibt mit dem Einsatz verknüpft.

## Bestehende Daten und Sicherheit

Die interne Datensatzstruktur `version:1` und die bisherigen Felder bleiben kompatibel. Neue Zeitstempel und Auswahlmodi sind zusätzliche optionale Felder. Vor dem Versionswechsel **ein Datenbankbackup** erstellen; danach V2.19 mit der bisherigen Datenbank öffnen. Alte Einsätze und Serviceberichte werden nicht automatisch umgeschrieben. Ein PDF-Vergleich ist niemals Exportvoraussetzung.

Der Datenbank-Speicherort (lokal/Cloud) ist von der Programmversion unabhängig. Eine lokale DB-Speicherung garantiert noch keinen abgeschlossenen Cloud-Abgleich; hierfür den Status unter „Speicherung & Sync“ prüfen. Bei einer GitHub Pages-Veröffentlichung `index.html` und `sw.js` gemeinsam ersetzen, damit auch Offline-Nutzer die neue Cache-Version laden.

## Technische Tests

`test_v216.py` enthält reproduzierbare Chromium-Tests der neuen Reise-/Zeit- und Abbruchabläufe. `test_regression.py` führt bestehende interne Selbsttests aus. `TESTPROTOKOLL.md` führt den Umfang auf. Für die Tests sind Python, BeautifulSoup, Playwright und Chromium erforderlich. Eine echte Cloud-Zwei-Geräte-Synchronisation und sämtliche PDF-Arten wurden hier nicht neu physisch geprüft.


## Version 2.19.0 – Ergänzungen

- Unter „Einsätze erfassen“ zeigen Kundeneinsätze den Status **rot: Nicht abgeglichen** oder **grün: PDF abgeglichen**. Nur ungeprüfte Einträge haben die Aktion „Service abgleichen“, welche die PDF-Auswahl im Reiter Servicebericht-Import öffnet. Der PDF-Abgleich bleibt freiwillig.
- „Eintrag anlegen“ hat keinen Zähler der freien Zeilen mehr. Zusätzliche Einträge am selben Tag sind weiterhin möglich.
- Technikerprofile werden ausschließlich in **Einstellungen** verwaltet. Der Alltag verwendet jeweils ein aktives Technikerprofil, weitere Profile können dort angelegt, ausgewählt, bearbeitet und archiviert/gelöscht werden.
- Im PDF-Import steht „Auswahl bestätigen und speichern“ am Ende der Kontrollliste. Nach erfolgreichem lokalen Speichern werden Vorschau, Dateiauswahl und Zuordnungsinformationen geleert – danach lassen sich direkt neue PDF-Dateien einlesen. Bereits gespeicherte Einträge bleiben erhalten.
- Eine dauerhaft oben sichtbare Statusleiste trennt **lokale Speicherung** und **Ordner-/Cloud-Synchronisation**. Sie enthält „Ordnerzugriff“, „Jetzt synchronisieren“ und „Details“. Nicht bestätigte Cloud-Synchronisation ist kein Fehler der lokalen Speicherung. Ordnerberechtigungen können erneut angefragt und unterschiedliche Dateistände verglichen werden; der Code überschreibt divergierende Datenbanken nicht ungefragt.

**Wichtige Einschränkung:** Eine automatische Geräte-übergreifende Cloud-Synchronisierung ist nur möglich, wenn der jeweilige Browser den benötigten dauerhaften lokalen Ordnerzugriff unterstützt und die lokale Cloud-Client-Software den Ordner tatsächlich synchronisiert. Wo dies nicht unterstützt wird (häufig auf Android), ist der bestehende manuelle .db-Datenbanktransfer notwendig. Der grüne bestätigte Ordnerstatus bedeutet nur, dass die verknüpfte Ordnerdatei nach dem Schreiben geprüft wurde – **nicht**, dass ein Cloud-Server oder anderes Gerät den Stand bereits übernommen hat.

Vor dem Update eine Datenbanksicherung exportieren.


## Version 2.19.0 – Bedienung und Datenintegrität

- Cloud-Symbol im Kopfbereich statt Dauerleiste: Ordnerzugriff und manuelle Synchronisation sind unter einem Symbol gebündelt; deutliche Warnhinweise erscheinen nur bei Fehlern oder Konflikten.
- Ordner- und Browserstände mit abweichenden Revisionen werden nicht überschrieben. Der Konfliktzustand blockiert weitere automatische Schreibversuche auch nach zusätzlichen lokalen Speichervorgängen; Auflösung nur durch bewusste Entscheidung unter „Speicherung & Sync“.
- Bei größeren lokalen Ständen wird im Vergleich besonders gewarnt, die ordnerseitige ältere Datei nicht unbedacht zu laden. Vor einer bewussten lokalen Veröffentlichung wird der Ordnerstand in einem getrennten Backup erhalten. Es findet **keine automatische Verschmelzung** von Einsätzen aus zwei Datenbanken statt.
- Unter „Einsätze erfassen“ ist „Nicht abgeglichen“ selbst der anklickbare Link zum PDF-Import; der separate Button entfällt. Bei fehlenden Start-/Enduhrzeiten öffnet der rote Link „Uhrzeiten nachtragen“ den bestehenden Einsatz.
- Bei PDF-Abgleichen ohne echte Beginn-/Enduhrzeiten bleiben vorhandene manuelle Uhrzeiten erhalten. Arbeitsdauer aus dem PDF kann mit der erfassten Arbeitsdauer abgeglichen und abweichend bestätigt werden.
- Die manuellen Arbeitsbeginn-/Endeuhrzeiten stehen auf dem PC nebeneinander. Zeitwahl und separate Tastatur-Eingabe sind möglich. Arbeit über Mitternacht wird beim Speichern bestätigt, das störende Enddatumfeld wird ausgeblendet.
- In „Speicherung & Sync“ wird die optionale Verbindung eines lokalen Datenbankordners erklärt. Ohne diese bleibt die lokale Browserdatenbank erhalten und man kann wie bisher einen Download als separate Sicherung anlegen. Android-/Browserbeschränkungen bleiben bestehen.
- Unter dem Servicebericht-Import wird kurz erklärt: regelbasierte Textauswertung ohne KI, Einsätze vergleichen, Stammdaten/Adressen übernehmen, Navigation öffnen und mit vorhandenen Kundendaten neuen Einsatz starten.

**Wichtig:** Vor Versionswechsel eine .db-Kopie außerhalb des Browser-Speichers sichern. Bei 199 lokalen Einsätzen gegenüber nur 7 in der Ordnerdatei niemals unkontrolliert den Ordnerstand laden. Cloud-Konflikte auf zwei realen Geräten wurden nicht end-to-end geprüft.


## Version 2.19.0 – automatische Einweg-Synchronisation und Konfliktempfehlung

- Bei eindeutigem gemeinsamem Revisionsanker und ausschließlich fortgeschriebener Ordnerdatei wird die aktuellere Datei automatisch in den Browser geladen. Davor wird die bisherige lokale SQLite-Datei als unabhängiges IndexedDB-Backup gesichert. Die Wochenansicht wird anschließend aktualisiert.
- Bei ausschließlich lokal fortgeschriebenem Stand bleibt das vorhandene sichere Verhalten erhalten: Ordnerdatei vor dem Schreiben nochmals einlesen und verifizieren, danach lokalen Stand hochladen.
- Die Prüfung läuft beim Start, beim Wiederöffnen der Anwendung und vor PDF-Sammelimporten; außerdem bei manueller Synchronisation. Vor der endgültigen PDF-Übernahme wird erneut geprüft.
- Bei offenen Eingaben oder einer unbestätigten PDF-Vorschau wird kein automatischer Cloud-Import durchgeführt. Bei nicht eindeutig bestimmbarer Änderungsrichtung bleibt die Synchronisation gesperrt.
- Die Konfliktansicht vergleicht lokal und in der Ordnerdatei tatsächlich enthaltene Einsatz-IDs sowie abweichende Datensätze und zeigt eine bedingte Empfehlung: Ordnerstand laden, lokalen Stand übernehmen oder beide getrennt sichern und Unterschiede prüfen. Eine größere Einsatzanzahl oder Revisionsnummer allein autorisiert niemals ein automatisches Überschreiben.
- Frühere Konfliktsperren können sich bei der Prüfung automatisch auflösen, wenn zweifelsfrei feststeht, dass nur ein Datenstand weitergeschrieben wurde. Die Datei wird gegen zwischenzeitliche Änderungen geprüft.
- Für eine Cloud-Übertragung zwischen Geräten ist weiterhin ein tatsächlicher Cloud-Sync des ausgewählten Ordners nötig. Auf Browsern ohne dauerhaften Ordnerzugriff funktioniert die lokale Datenbank mit separatem .db-Import/Export, nicht die automatische Dateisynchronisierung.

**Unbedingt zuerst eine externe .db-Sicherung erstellen, insbesondere falls auf einem Gerät 7 und auf dem anderen 201 Einsätze angezeigt werden.** Die App führt divergierende Einsätze nicht automatisch zusammen.
