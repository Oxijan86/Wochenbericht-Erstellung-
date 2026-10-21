# Wochenbericht Lovrencic – Version 2.13.0

Offlinefähige HTML-Anwendung für die mobile Erfassung von Fahrten, Pausen, Arbeitszeit und Wochenberichten im ursprünglichen Excel-Format.

## Neu: Fahrten- und Einsatzassistent

**Dashboard → „Neuen Einsatz erfassen“** öffnet einen mobilen Schritt-für-Schritt-Assistenten:

1. Hinfahrt starten. Kilometer und Reisezeit sind einzeln erfassbar; der Fahrt-Zeitstempel wird dauerhaft gespeichert.
2. Bei Ankunft die Hinfahrt abschließen. Die Zeit wird aus dem Zeitstempel vorgeschlagen und kann korrigiert werden.
3. Kunde/Ort eintragen und mit **„Arbeitszeit starten“** die Uhrzeit speichern.
4. Während einer laufenden Fahrt oder Arbeit mit **„Pause starten“** unterbrechen und mit **„Pause beenden / Fortsetzen“** weiterarbeiten. Unterbrechungen werden getrennt mit Zeitstempeln gespeichert und von der jeweiligen Zeit abgezogen.
5. **„Arbeit beenden“** speichert die Endzeit. Anschließend zwischen **„Rückfahrt starten“** und **„Zum nächsten Kunden fahren“** wählen.
6. Auf der Rückfahrt werden Kilometer und Zeit der Hinfahrt als Vorschlag übernommen. Erst **nach der ausdrücklichen Bestätigung** gehen sie in die Gesamtwerte ein. Alternativ kann die tatsächlich gemessene Fahrtzeit übernommen werden.
7. **„Zum nächsten Kunden fahren“** beendet den bisherigen Einsatz ohne erfundene Rückfahrt und beginnt die neue Hinfahrt als eigenständigen Einsatz.

Beim Schließen des Assistenten bleiben **bestätigte Schritte** und eine gerade aktive Pause erhalten; im Dashboard ist der Einsatz wieder aufrufbar.

## PDF-Abgleich und Reisezeit-Abweichungen

Im vorhandenen Reiter **Datenimport** bleiben PDF-, M365- und Excel-Import erhalten. Vorhandene Einsätze werden abgeglichen. Wenn die PDF-Reisezeit vom manuell erfassten Wert abweicht, erscheint ein Hinweis zur Überprüfung auf Stau/Umleitung und gegebenenfalls zur internen Klärung der Kundenabrechnung. Es wird **kein Ticket automatisch erzeugt** und kein vorhandener Wert ohne Auswahl aktualisiert.

## Datenmodell und Kompatibilität

Die zusätzlichen Angaben liegen im optionalen Feld `entry.trip` und enthalten Phase, Fahrtdaten, Start-/Endzeitstempel und Pausenintervalle. `entry.km` und `entry.travel` behalten die bisherige Bedeutung als **bestätigte Gesamtkilometer bzw. Reisezeit**. Nicht abgeschlossene Rückfahrten werden nicht als Gesamtwert addiert. Die bestehende `wochenberichte.db` bleibt lesbar, frühere Einträge ohne `trip` bleiben unverändert, das Excel-Layout bleibt erhalten.

Die neue Fahrt-zum-Kunden-Bedienung ist eine Ergänzung zur weiterhin vorhandenen regulären manuellen Erfassungsmaske.

## GitHub Pages

`index.html`, `sw.js`, `README.md` und `.nojekyll` ins Stammverzeichnis des Repositorys hochladen; unter **Settings → Pages** `main` und `/ (root)` auswählen. Cache wird über `wochenberichte-static-v2.13.0` aktualisiert.

## Wichtige Grenzen

- Auf dem Smartphone kann der Browser seine Ordner-Berechtigung beim Neustart verlieren; zunächst lokal speichern, Ordner ggf. erneut freigeben.
- Dateisynchronisation ist keine serverseitig atomare Mehrgerätesynchronisation.
- Im Assistenten zählen bestätigte Schritte. Erst erfasste, noch nicht bestätigte Felder gelten nicht als fertig gespeichert.
- Die Rundung erfolgt auf Viertelstunden, aktive Pausen enthalten rohe Zeitstempel.
- Die tatsächliche Öffnung in Android Chrome, Excel Mobile und ein Cloud-Abgleich auf zwei physischen Geräten wurden hier **nicht getestet**.

Vor dem Aktualisieren der Anwendung bitte `wochenberichte.db` sichern.
