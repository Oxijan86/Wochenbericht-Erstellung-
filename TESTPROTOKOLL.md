# Testprotokoll Wochenbericht Lovrencic V2.23.0

## Automatisierte Prüfungen (23.10.2026)

- JavaScript-Syntaxprüfung per Node.js für alle fünf eingebetteten Skripte erfolgreich.
- **31 von 31 internen Selbsttests erfolgreich:** `test_regression.py`.
- Vorhandene Browser-Regressionen erfolgreich: `test_v216.py`, `test_v217.py`, `test_compat_v217.py`, `test_v218.py`, `test_v218_regression.py`, `test_v219.py`, `test_v221.py`, `test_v222.py`. Der Versionsvergleich in `test_v219.py` wurde an V2.23 angepasst.
- **Neue Browserprüfung `test_v223.py` erfolgreich:** Unabhängige Auswahl pro PDF, Technikerpositionen nur für ausgewählte Person, vollständiges Überspringen eines PDFs, Einbeziehung der anderen PDFs, auch eindeutige PDFs überspringbar, kein überflüssiger Bestätigungshaken, keine unbemerkte Übernahme leerer Positionen, bei Überspringen aller PDFs keine Speicherung, explizites Auslassen fehlerhafter PDFs, Bedienung im mobilen Layout.
- Durchgehender Test mit simulierten PDF-Datensätzen: Aus einem Stapel mit drei PDFs zwei übersprungen, eines bewusst importiert. Ausschließlich der ausgewählte Einsatz und dessen PDF-Nachweis wurden lokal gespeichert; danach war die Importauswahl zurückgesetzt.
- ZIP-Struktur und Integritätsprüfung bei der Paketgenerierung durchgeführt.

## Noch mit echten Dateien/Geräten zu prüfen

- Der vorhandene `test_pdf_workflow.py` benötigt echte digitale RONDO-PDFs, die hier nicht bereitgestellt wurden.
- `test_special.py` benötigt eine externe Excel-Beispieldatei. Nicht ausgeführt.
- Cloud-Synchronisation mit deinem tatsächlichen OneDrive-Ordner auf PC und Smartphone ist damit nicht end-to-end geprüft.

**Vor dem Update eine separate lokale Sicherung der produktiven `.db`-Datei anfertigen; anschließend die tatsächlichen Einsätze und den Ordnerstatus prüfen.**
