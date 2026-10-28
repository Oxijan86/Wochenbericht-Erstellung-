# V2.24.1 – 28.10.2026

- Interaktive Kundensuche im Einsatzassistenten: Namens- und Nummern-Fragmente, Standorte und Adressen, mobile Tastatur, getrennte Filialen.
- Übergreifender Uhrzeitkorrektur-Dialog für alle sechs Zeitstempel; Zeitfolgen und Pausen validiert; automatische Reisezeitberechnung nach Korrektur, PDF-Prüfnachweise bleiben unverändert bzw. nur als nachbearbeitet markiert.
- V2.24-Mehrtagelogik an den tatsächlichen PDF-Direktimport angebunden. Bei M365-Import nicht mehr irrtümlich ausgelöst.
- PDF-Enddatum, maximal 14 Tage Rückschau, gemeinsamer Gesamtstunden-/Reisezeit-/Kilometervergleich; Zustimmung für den Gesamt-Abgleich ausdrücklich erforderlich. Alle Tageswerte werden unverändert gelassen; PDF-Nachweise für alle Tage.
- Service-Worker-Cacheversion V2.24.1 und `index.html`-Registrierung synchronisiert; Hilfetext aktualisiert, keine Datenbankmigration.

# V2.24 – Mehrtägiger PDF-Gesamtabgleich (Vorversion)

- Erste Implementierung für mehrere Tage gleicher Ticketnummer und passendem Kunden.
- PDF-Werte als Gesamtwerte, Tageswerte bleiben erhalten, gemeinsam geprüfte Tage.

# V2.23.0 – 23.10.2026

- Pro RONDO-PDF „Positionen übernehmen und abgleichen“ oder „Diesen Bericht vollständig überspringen“.
- Technikerzuordnung ohne zusätzlichen Pflicht-Bestätigungshaken.
- Übersprungene PDFs werden nicht als Einsätze oder Nachweise gespeichert; übrige PDFs bleiben im Stapel.
- Fehlerhafte PDFs und leere Positionsauswahl können nicht unbemerkt importiert werden.

# V2.22 – 22.10.2026

- Kalenderwoche und Stundenübersicht auf Eingabe- und Exportansicht begrenzt.
- PDF-Arbeitsdauer plus Pause als automatisch berechneter Enduhrzeitvorschlag; kein Überschreiben gespeicherter manueller Zeiten.

# V2.21 – 22.10.2026

- PDF-Arbeitsdauer-Differenzen ab 15 Minuten als Hinweis, ab 30 Minuten deutliche Warnung ohne Export-Sperre.
- Vollständigkeitsprüfung für echte Uhrzeiten von PDF-Dauerabweichungsprüfung getrennt.
- Historische Serviceberichte werden wieder regulär mit Dublettenprüfung in die Historie aufgenommen.

# V2.20 – 22.10.2026

- Netto-Arbeitsdauer im PDF mit manuellen Zeiten vergleichen und Endzeitvorschlag berechnen.
- Korrektur ohne Verlust des PDF-Nachweises und Rücksprung in die Wochenansicht.
