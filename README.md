# Wochenbericht Lovrencic – Version 2.6.0

GitHub-Pages-fähige Offline-Wochenberichts-Anwendung. `index.html` und `sw.js` ins Repository-Stammverzeichnis hochladen. Öffentliche Datei enthält eine anonymisierte Excel-Vorlage; lokale Nutzerdaten liegen ausschließlich im jeweiligen Browser (IndexedDB) bzw. in einer bewusst verbundenen `.db`-Datei, nicht im Repository.

## Änderungen gegenüber V2.5

- **Datum beim Stempeln**: „Beginn ab jetzt“ und „Beenden ab jetzt“ setzen beide das aktuelle Tagesdatum und die aufgerundete Viertelstunde. Der Start setzt den Fokus auf den Kunden. Wechsel in aktuelle KW erhält bisherige Formulareingaben. Die Original-Excel-Vorlage erlaubt nur Montag bis Freitag.
- **Laufende Einsätze**: Anfangszeit kann ohne Endzeit gespeichert werden. Ticket und weitere Felder sind optional. Gespeicherte Einträge sind in der Tagesliste als laufend markiert; „Jetzt stoppen“ beendet am selben Datum. Unvollständige Formulare werden fortlaufend als Entwurf in IndexedDB gespeichert. Bestätigte Einträge gelten erst nach erfolgreichem dauerhaften Speichern als gespeichert.
- **Kundenstamm (eigener Reiter)**: Kunden aus vorherigen Einsätzen werden einmalig als separate Datensätze übernommen, getrennt nach Standorten. Neu erfasste Einsätze und importierte M365-Zeilen aktualisieren zuletzt vorhandene Kilometer- und Reisezeitwerte. **Alte Einsatz- und Wochenberichtszeilen bleiben unverändert.** Kundenliste mit Suche, Sortierung, Übernahme, Bearbeiten und Löschen (ausschließlich Stammdatensatz).
- **Mobile UI**: Größere Menü-Icons und Schaltflächen, Abschlussdialog zusätzlich über Hamburger-Menü.
- **Version**: 2.6.0 zentral in App definiert, Service-Worker-Cache ebenfalls 2.6.0.

## Einrichten und aktualisieren

1. Vor der Aktualisierung in V2.5 `wochenberichte.db` herunterladen.
2. Auf GitHub die `index.html`, `sw.js`, `README.md`, `.nojekyll` aus dem Schnellupload ersetzen.
3. Auf der bisherigen Pages-Adresse öffnen, damit die lokale IndexedDB unter demselben Ursprung erhalten bleibt. Version 2.6.0 im Kopf prüfen.
4. Bei separater HTML-Datei oder anderem Ursprung vorhandene `wochenberichte.db` über „Vorhandene Datenbank öffnen“ importieren.

Speicherung, Ordner-Synchronisation, Konfliktschutz, Backup, Excel-Export und M365-Import bleiben Bestandteil der Anwendung. Nutzer müssen Browser-Zugriffsrechte für lokale Ordner ausdrücklich freigeben. Automatische synchronisierte Ordner stehen auf Android je nach Browser nicht zur Verfügung. Browserdownloads sind separate Kopien. Gleichzeitiges Mehrgeräte-Schreiben wird nicht garantiert.

## Veröffentlichung

GitHub `Settings > Pages` : Deploy from a branch, `main`, `/ (root)`. GitHub-URL: `https://oxijan86.github.io/Wochenbericht-Erstellung-/` (nach Upload/Pages-Build).

Siehe `TESTPROTOKOLL.md` für lokale Tests und Einschränkungen.

## Prüfbericht

Die ergänzenden Browser- und Regressionstests sind in `TESTPROTOKOLL.md` dokumentiert. Browsernavigation zu einer realen lokalen/HTTPS-Testadresse sowie ein echtes Android-Gerät waren in der Testumgebung nicht verfügbar. Ein echter Zwei-Geräte-Synchronisationstest ist nicht behauptet.
