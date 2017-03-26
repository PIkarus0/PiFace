# PiFace Digital 2 Modul
Das Programm stellt verschiedene Funktionen für das PiFace Digital 2 Modul bereit<br>
- einzelnen Eingang einlesen<br>
- einzelnen Ausgang einlsen<br>
- 8 Eingänge einlesen<br>
- 8 Ausgänge schreiben<br>
- 16 Zeiten starten/auswerten/rücksetzen<br>
- Ansteigende Flanken auswerten<br>
- Abfallende Flanken auswerten<br>
- Schiebe 1 Bit nach links (Byte) mit Übertrag<br>
- Schiebe 1 Bit nach rechts (Byte) mit Übertrag<br>
## Das Demoprogramm
Mit Eingang 0 wird der Ausgang 0 gesetzt oder zurückgesetzt. Gleichzeitig startet die Zeit 0. Ist diese abgelaufen, 
so wird Ausgang 1 gesetzt und Zeit 1 gestartet. Nach ablauff von Zeit 1 wird Ausgang 1 wieder ausgeschaltet.<br>
Mit dem Eingang 1 kann zum zweiten Demo umgeschaltet werden. Wird Eingang 0 betätigt so wird zeitgesteuert schiebe links Bit
bzw. schiebe rechts Bit gestartet. Wird ein Bit aus dem Byte geschoben, so wird die Richtung umgeschaltet (Nightrider Effekt).
Eingang 2 schaltet alle Ausgänge aus.<br>
## Installation auf dem Raspberry Pi
Benötigt werden die Dateien:<br>
- pifacecommon-master<br>
- pifacedigitalio-master<br>
