# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 15:13:46 2024

@author: Jonas
"""

import os

def schreibe_dateinamen_in_datei(ordnerpfad, ausgabedatei):
    try:
        # Überprüfen, ob der Ordnerpfad existiert
        if not os.path.isdir(ordnerpfad):
            print(f"Der Ordnerpfad '{ordnerpfad}' existiert nicht.")
            return
        
        # Öffnen der Ausgabedatei im Schreibmodus
        with open(ausgabedatei, 'w') as datei:
            # Durchlaufe alle Dateien im Ordner
            for dateiname in os.listdir(ordnerpfad):
                dateipfad = os.path.join(ordnerpfad, dateiname)
                # Überprüfen, ob es sich um eine Datei handelt (nicht um einen Ordner)
                if os.path.isfile(dateipfad):
                    datei.write(dateiname + '\n')
        
        print(f"Die Dateinamen wurden erfolgreich in '{ausgabedatei}' geschrieben.")
    
    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")

# Beispielverwendung
ordnerpfad = r'C:\Users\Jonas\Documents\MASCOT\SourceCode\pyMANGA-1\MyModel\Scenarios\OnePlant'  # Pfad zum Ordner, dessen Dateinamen gelesen werden sollen
ausgabedatei = 'dateinamen.txt'  # Name der Ausgabedatei
schreibe_dateinamen_in_datei(ordnerpfad, ausgabedatei)