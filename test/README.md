# unit tests

Im Ordner test in der Hauptebene des Programms befindet sich der Modultest.

## Testablauf

Zur Durchführung eines automatischen Modultests steht hier einmal ein Test für kleinere, weniger komplexere Setups und einer für größere, komplexere Setups zur Verfügung. Für die längere Modelllaufzeit im Typ Large Setup ist vor allem die Berechnung der Belowground Competition mit Hilfe der numerischen Grundwassermodellierungssoftware OpenGeoSys verantwortlich. Das Ausführen der Tests unterscheidet sich aber nicht, beide werden wie im nächsten Absatz beschrieben gestartet. Auch der Testablauf ist identisch. Im ersten Teil wird lediglich überprüft ob das Setup bis zum Ende berechnet werden kann. Erst im zweiten Teil werden dann die berechneten Ergebnisse mit hinterlegten "Musterlösungen" verglichen. Falls es zu einem Fehler bei der Berechnung mit einem der Testsetups kommen sollte wird der Nutzer am Ende darüber informiert bei welchem Setup und welchem Teil des Tests das Problem auftrat.

## Ausführung der Modultests

Der Modultest ist so konfiguriert, dass er von der Hauptebene des Programms aus gestartet wird. Um den Modultest auszuführen werden die beiden Dateien test/SmallTests/test_small.py und test/LargeTests/test_large.py gestartet.
