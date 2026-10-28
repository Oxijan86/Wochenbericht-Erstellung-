# V2.23.0 – 23.10.2026

- Pro RONDO-PDF ist unabhängig von der Technikerzuordnung ausdrücklich wählbar: „Positionen übernehmen und abgleichen“ oder „Diesen Bericht vollständig überspringen“.
- Zusätzliche Pflicht-Checkbox „Ich habe die Positionen geprüft…“ aus der Technikerzuordnung entfernt. Übernahme und Abgleich bleiben separate, bewusste Schritte.
- Übersprungene PDFs werden von Einsatzvorschau und PDF-Nachweisspeicherung ausgeschlossen. Übrige PDFs desselben Stapels bleiben erhalten.
- Wenn alle PDFs übersprungen werden: zurück zur neuen Dateiauswahl, keine Änderungen an der Datenbank.
- Sicherheitsprüfung: Ein Bericht mit null ausgewählten Positionen wird nicht leer importiert; fehlerhafte PDFs erfordern weiterhin den expliziten Ausschluss.
- In der Hilfe neue Bedienung erklärt. Versionskennung und Offline-Cache aktualisiert. Datenbankformat unverändert.

# V2.22 – 22.10.2026

- Kontextabhängige Anzeige der KW- und Stundenübersicht nur in Eingabe- und Exportansicht.
- Automatischer Endzeitvorschlag nach Eingabe des Beginns mit PDF-Nettozeit und Arbeitspause.
- Neu berechnen bei Änderung des vorgeschlagenen Beginns/Pause, ohne manuell gespeicherte Endzeiten zu überschreiben.
- Vor dem Speichern sichtbar als nicht überprüfter Vorschlag gekennzeichnet.

# Änderungsprotokoll

## V2.21.0 – 22.10.2026
- PDF-Abweichung ab 30 Minuten: deutliche, aber nicht sperrende Exportwarnung. 15–29 Minuten einfacher Hinweis.
- Korrektur des Exports: Begründete Ausnahme nur für fehlende echte Uhrzeiten erforderlich, nicht für die PDF-Dauerabweichung.
- Hinweis auf Differenz und direkte Einsatzkontrolle im Bereich „Wochenbericht / Export“.
- Sondermodus „Nur Kundenstamm ergänzen“ entfernt; historische PDFs landen wieder regulär in der Einsatzhistorie, mit Dubletten-/Zuordnungsprüfung.
- Anleitung und Hilfebereich aktualisiert; Datenschema und Synchronisationslogik unverändert.

## V2.20.0 – 22.10.2026
- PDF-Arbeitsdauer und tatsächliche Zeit unter dem Eingabefeld vergleichen; übernehmbarer Endzeitvorschlag inklusive Pause.
- Rücksprung in die Wochenansicht nach Korrektur, ursprüngliche Uhrzeiten und PDF-Nachweise bleiben bestehen.
- Exportprüfung auf fehlende Uhrzeiten, dokumentierte Ausnahmen und deutliche PDF-Dauerabweichung.


## V2.24 – Mehrtägiger PDF-Gesamtabgleich
- Erkennt mehrere gespeicherte Einsatztage mit gleicher Ticketnummer und passendem Kunden bis zum PDF-Enddatum (maximal 14 Tage).
- PDF-Zeiten und Kilometer als Gesamtsummen; keine Überschreibung der Tagesbuchungen.
- Nach Abschluss werden alle zugehörigen Einsatztage als PDF-geprüft dokumentiert.
- Bestehender PDF-Import für einzeltägige Einsätze bleibt erhalten.
