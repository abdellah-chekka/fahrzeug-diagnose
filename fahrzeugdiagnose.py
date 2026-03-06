import json
import random
from datetime import datetime

class FahrzeugDiagnose:
    def __init__(self):
        self.sensoren = {
            "geschwindigkeit": {"min": 0, "max": 200, "einheit": "km/h"},
            "motortemperatur": {"min": 70, "max": 110, "einheit": "°C"},
            "reifendruck": {"min": 2.0, "max": 2.8, "einheit": "bar"},
            "batterie": {"min": 10, "max": 100, "einheit": "%"}
        }
        self.fehler = []
    
    def generiere_daten(self):
        """Simuliert eingehende Sensordaten"""
        daten = {
            "zeit": datetime.now().strftime("%H:%M:%S"),
            "geschwindigkeit": random.randint(0, 220),
            "motortemperatur": random.randint(65, 120),
            "reifendruck": round(random.uniform(1.8, 3.0), 1),
            "batterie": random.randint(5, 100)
        }
        return daten
    
    def pruefe_sensor(self, name, wert):
        """Prüft ob Sensorwert im Normalbereich liegt"""
        grenzen = self.sensoren[name]
        if wert < grenzen["min"] or wert > grenzen["max"]:
            fehler_msg = f"{name}: {wert}{grenzen['einheit']} (OK: {grenzen['min']}-{grenzen['max']}{grenzen['einheit']})"
            self.fehler.append(fehler_msg)
            return False
        return True
    
    def diagnose(self, anzahl_messungen=5):
        """Führt komplette Fahrzeugdiagnose durch"""
        print("\n" + "="*50)
        print("FAHRZEUGDIAGNOSE GESTARTET")
        print("="*50)
        
        for i in range(anzahl_messungen):
            daten = self.generiere_daten()
            print(f"\n Messung {i+1}: {daten['zeit']}")
            
            fehler_gefunden = False
            for sensor in self.sensoren:
                if not self.pruefe_sensor(sensor, daten[sensor]):
                    fehler_gefunden = True
            
            status = "FEHLER" if fehler_gefunden else " OK"
            print(f"Status: {status}")
        
        # Zusammenfassung
        print("\n" + "="*50)
        print("DIAGNOSE-ERGEBNIS")
        print("="*50)
        
        if self.fehler:
            print(f"Gefundene Fehler ({len(self.fehler)}):")
            for f in self.fehler:
                print(f"  • {f}")
            
            # Speichere Fehlerbericht
            with open("fehlerbericht.json", "w") as f:
                json.dump({
                    "zeitpunkt": datetime.now().isoformat(),
                    "anzahl_fehler": len(self.fehler),
                    "fehler": self.fehler
                }, f, indent=2)
            print(f"\nFehlerbericht gespeichert: fehlerbericht.json")
        else:
            print("Keine Fehler gefunden - alles OK!")
        
        return self.fehler

# Hauptprogramm
if __name__ == "__main__":
    diagnose = FahrzeugDiagnose()
    fehler = diagnose.diagnose(anzahl_messungen=10)