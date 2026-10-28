
## V2.24.3: Testläufe
- JavaScript-Syntax sämtlicher Inline-Skripte und des Serviceworkers: bestanden.
- `test_regression.py`: 31/31 interne Selbsttests bestanden.
- `test_v2242.py`: 28-Tage-Suche, Ticketnachtrag und PDF-Schutz in Desktop- und Mobilansicht bestanden.
- `test_v2241.py`: ursprüngliche Assistent-/PDF-/Mehrkundentests in Desktop- und Mobilansicht bestanden (Anzeige umfasst nun zusätzlich Pausenfelder).
- `test_v2243.py`: automatische Ankunft/Arbeitsbeginn-Verknüpfung, Änderungsverknüpfung, Pausennachtrag, individuelle Abschaltung auf PC/Mobilansicht bestanden.
- Realbetrieb auf Android mit echten PDFs/Cloud-Synchronisation bleibt ungetestet.

# Testprotokoll – Wochenbericht Lovrencic V2.24.2

## Zusätzliche Tests V2.24.2 (28.10.2026)

- `test_v2242.py`: echte Chromium-Klicktests auf Desktop-Breite 1280 px und mobilem 390-px-Touch-Viewport. Belegt 28-Tage-Grenze, getrennte Auswahl gespeicherter Einsatztage, Vorschläge ohne Ticket, Ausschluss eines anderen Tickets/Kunden, Pflichteinbeziehung des PDF-Endtags und ausdrückliche Zustimmung.
- Nach Bestätigung wurden nur an zwei ausgewählten Tagen PDF-Prüfnachweise gesetzt. Die fehlende Ticketnummer wurde ausschließlich am ausgewählten Tag ergänzt. Nicht ausgewählte Einsätze, andere Tickets und **sämtliche bisherigen Tages-Kilometer, Fahrtzeiten und Arbeitszeiten** blieben unverändert.
- `test_v2241.py` weiterhin bestanden: Kundensuche, Korrektur von Uhrzeiten, mehrtägiger PDF-Abgleich mit drei Tagen, Abbruch und Mehrkundenfahrten, jeweils auch mit Mobile-Viewport.
- `test_regression.py`: 31/31 interne Tests bestanden; `test_v2241_codec.py`: SQLite-Roundtrip und `PRAGMA quick_check = ok`. Weitere bestehende Tests: `test_compat_v217.py`, `test_v216.py`, `test_v217.py`, `test_v218.py`, `test_v218_regression.py`, `test_v219.py`, `test_v221.py`, `test_v222.py`, `test_v223.py` bestanden. In `test_v219.py` ausschließlich die fest eingetragene erwartete Versionsnummer aktualisiert.
- JavaScript-Syntaxprüfung aller fünf Inline-Skripte erfolgreich. `sw.js`-Cachekennung entspricht 2.24.2. Die bisher beschriebenen Grenzen (kein reales RONDO-PDF, kein echtes Android-Gerät, kein OneDrive-/Offline-End-to-End-Test, keine produktive Datenbank) gelten weiter.

**Ausgangsbasis dieser Folgeversion:** vom Nutzer hochgeladenes V2.24.1-ZIP, 21 Dateien. GitHub wurde nicht verändert.

---

**Prüfdatum:** 28.10.2026. **Ausgangsbasis:** Repository `Oxijan86/Wochenbericht-Erstellung-`, `main`, ursprüngliche `index.html` aus V2.24 (Git-Blob `23b1007753133358efbc2357204e7da922a86f85`). Weder GitHub noch produktive Datenbank wurden geändert.

## Behobene Probleme

1. Einsatzassistent/Dashboard verwendete eine native Scroll-Kundenauswahl statt einer mobil geeigneten Tastatur-Suche. Jetzt Live-Suche nach Name, Kundennummer, Standort und Adresse mit getrennter Standortauswahl und Übernahme der Stammdaten; neue Standorte weiterhin möglich.
2. „Uhrzeiten korrigieren“ bot nur phasenweise Zeitfelder an. Jetzt eigener Korrekturdialog für alle im jeweiligen Einsatz erfassten Zeitstempel. Zeitfolge, Pausen und Datumswechsel werden validiert, gemessene Reise-/Arbeitszeiten neu berechnet. PDF-Prüfnachweise bleiben dokumentiert.
3. V2.24 hatte den Mehrtages-Gesamtabgleich im M365-Textimport angeordnet, aber nicht im realen RONDO-PDF-Direktimport. Die PDF-Vorschau erkennt nun den zusammengehörigen Ticket-/Kunden-/Zeitraum, zeigt Summen/Abweichungen und erfordert ein ausdrückliches „Gesamtsummen geprüft“, bevor alle Tagesnachweise erstellt werden. Einzelne Tageswerte werden nicht überschrieben.
4. Versions-/Cache-Kennung jetzt `2.24.1`, statische SW-App-Aktualisierung netzbevorzugt, bisheriger IndexedDB-Datenbankname und das SQLite-Datenformat unverändert.

## Erfolgreich ausgeführt

- **JavaScript-Syntax:** alle fünf Inline-Skripte der HTML-Anwendung und `sw.js`, `node --check`, fehlerfrei.
- **Interne Selbsttests:** 31/31 bestanden, `test_regression.py`.
- **Alt-/Regressionstests:** `test_compat_v217.py` (19/19), `test_v216.py`, `test_v217.py`, `test_v218.py`, `test_v218_regression.py`, `test_v219.py`, `test_v221.py`, `test_v222.py`, `test_v223.py` jeweils erfolgreich unter Headless Chromium. Sie decken unter anderem Start, Hinfahrt und Arbeitspausen, Ankunft, Arbeitsbeginn/-ende, Rückfahrt, Kundenwechsel, Abbruch, vorhandene PDF-Markierung, Dialoge, Export-/Import-Logik und Sync-Konfliktschutz ab.
- **Angepasste Alt-Testannahmen:** `test_v219.py` erwartete fest die alte Version 2.23.0; Erwartung auf 2.24.1 geändert. `test_v216.py` zeigte durch den mittlerweile gewechselten Kalenderwochenkontext den geprüften Oktober-Einsatz nicht im geöffneten Tabellenmonat; Test stellt nun die KW des Beispieldatums ein. Sonstiger Ablauf unverändert. Beide Tests danach vollständig erfolgreich. Das Kalenderwochen-Problem trat auch mit der unveränderten V2.24-App auf.
- **Neue echte Browser-Interaktionstests `test_v2241.py`:** PC-Viewport 1260×960 und mobiler Chromium-Viewport 390×844 mit Touch-Events. Tastatursuche nach Kundennummer, Teilbegriff/Mischschreibung, separate Filialen, Auswahl/Adressübernahme, gesamter Korrekturdialog mit sechs Zeitstempeln, Uhrzeitänderungen, Fehler bei ungültiger Folge, PDF-Nachweis nach Korrektur, gezielter Abbruch, mehrfache Aufteilung von Mehrkunden-Fahrten ohne Doppelzählung – bestanden.
- **PDF-Gesamtabgleich, synthetische Daten:** drei gespeicherte Tagesberichte vom 26.–28.10., Ticket gleich, 18 h Arbeitszeit / 4 h Reisezeit / 240 km im simulierten Servicebericht. PDF-Vorschau erzeugt Gesamtgruppe und verlangt eine Entscheidung. Nach ausdrücklich gesetzter Bestätigung wurden 3/3 Tagesberichte als geprüft markiert, alle individuellen Tageswerte unverändert; erneute Prüfung desselben Dokuments erzeugt keine doppelten Nachweise. `test_v2241.py` erfolgreich.
- **SQLite-Kompatibilität `test_v2241_codec.py`:** synthetische Bestandsdaten mit Kunden, Einsatz und PDF-Prüfvermerk über `WBSqlite.encode`/`decode` unverändert auslesbar; SQLite-Standardtreiber kann `app_state` lesen; **`PRAGMA quick_check = ok`**, beschädigte/abgeschnittene Datei wird abgewiesen.
- **ZIP-Struktur:** alle Dateien aus dem bisherigen V2.24-GitHub-Paket übernommen; nur Hauptdateien und dokumentierte Testanpassungen verändert. Das neue Paket ist auf Lesbarkeit und vollständiges Auspacken prüfbar.

## Nicht ausgeführt oder technisch eingeschränkt

- **Keine Original-RONDO-PDFs bereitgestellt.** `test_pdf_workflow.py` benötigt echte digital lesbare Serviceberichte unter `rondo_pdf_probe/` und wurde nicht erfolgreich ausgeführt. Der Mehrtages-PDF-Test verwendet ausschließlich synthetische importähnliche Datensätze; er ersetzt keine PDF-Parser- oder Geräteprüfung.
- **`test_special.py`:** benötigt die optionale externe Excel-Musterdatei; nicht ausgeführt.
- **Keine echte Android-Hardware:** Mobilbedienung nur mit emuliertem Chromium-Viewport/Touch geprüft; insbesondere native Tastatur-/IME-Bedienung bitte am eigenen Gerät kontrollieren.
- **Kein produktiver OneDrive-Ordner/Ordnerfreigabe**, kein Multi-Geräte-Synchronisations-End-to-End-Test.
- **Kein echter HTTP-/Service-Worker-Offline-Reload:** Die lokale Chromium-Umgebung sperrt Navigationen mit `ERR_BLOCKED_BY_ADMINISTRATOR`. `sw.js` ist syntaxgeprüft und quellcodekontrolliert, die Installation/Aktivierung und Cache-Lebensdauer wurden nicht in einem echten Offline-Deployment verifiziert.
- **Keine produktive Datenbank / keine echten Nutzerdaten geöffnet.** Persistenz wurde durch vorhandene mocked-save-Browsertests, SQLite-Roundtrip und Strukturprüfung abgesichert. Echter IndexedDB-Reload im normalen HTTP-Browser konnte hier nicht ausgeführt werden. Bitte vor dem Upload die produktive `wochenberichte.db` sichern und nach dem Update eine Stichprobe im eigenen Browser prüfen.
- **Nicht jeder Button als separater Klickpfad end-to-end getestet.** Alt-Regressionen decken die meisten zentralen Assistenten- und Verwaltungsfunktionen ab; der neue PDF-Test setzt die explizite Entscheidung im Testautomaten programmatisch und testet anschließend die reale Abgleichfunktion. Nicht automatisch getestete Einzelfälle bleiben als manueller Abnahmetest bestehen.

## Benutzerprüfung vor produktiver Verwendung

1. `wochenberichte.db` über „Speicherung & Sync“ separat sichern und die Sicherung unabhängig aufbewahren.
2. `index.html` und `sw.js` zusammen nach GitHub hochladen, im Browser Seite neu laden und **Version 2.24.2** bestätigen.
3. Alten Einsatz öffnen; Kunden, ursprüngliche Uhrzeiten und PDF-Prüfnachweise auf Vollständigkeit kontrollieren.
4. Einen Probe-Einsatz starten, Kundenname und Filiale eintippen, dann abbrechen; prüfen, dass kein fremder Eintrag gelöscht wird.
5. Korrektur an einem bestehenden Einsatz durchführen, neu laden und Zeiten/Nettozeit/Pausen prüfen.
6. Mit einem echten mehrtägigen RONDO-PDF die Gesamtabgleichvorschau und grünen Haken kontrollieren; vor Bestätigung muss der Vergleich ausbleiben.
7. Ggf. Online-/Offline-Aufruf und OneDrive-Synchronisation auf PC und Smartphone testen, ohne Website-Daten/IndexedDB zu löschen.
